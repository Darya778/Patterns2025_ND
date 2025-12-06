from Src.Core.abstract_logic import abstract_logic
from Src.Core.observe_service import observe_service
from Src.Core import log_levels
from Src.settings_manager import settings_manager
from datetime import datetime
import os, sys

class logging_service(abstract_logic):
    """
    Служба регистрации на основе наблюдателей.
    Прослушивает события с именем 'log' или прямые вызовы через observe_service.create_event('log', {...})
    Ожидаемые параметры: dict with keys:
        - level: 'DEBUG'|'INFO'|'ERROR' (без учета регистра)
        - message: str
        - meta: необязательный dict с дополнительными данными (например, структура запроса)
    Он также поддерживает вызов с именами событий: 'LOG_DEBUG','LOG_INFO','LOG_ERROR'
    """
    def __init__(self):
        super().__init__()
        observe_service.add(self)
        # cache settings
        self.reload_settings()

    def reload_settings(self):
        try:
            sm = settings_manager()
            if not sm.settings:
                sm.file_name = os.path.join(os.getcwd(), 'settings.json')
                sm.load()
            s = sm.settings
        except Exception:
            s = None
        # defaults
        self.level = getattr(log_levels, 'INFO')
        self.mode = 'file'
        self.log_dir = os.path.join(os.getcwd(), 'logs')
        self.format = '{date} [{level}] {message} {meta}'

        if s is not None:
            cfg = getattr(s, 'logging', None) or {}
            level_name = cfg.get('min_level','INFO')
            self.level = getattr(log_levels, level_name.upper(), log_levels.INFO)
            self.mode = cfg.get('mode','file').lower()
            self.log_dir = os.path.abspath(cfg.get('directory', self.log_dir))
            self.format = cfg.get('format', self.format)

    def handle(self, event: str, params):
        super().handle(event, params)
        level = None
        msg = None
        meta = None
        if isinstance(event, str) and event.startswith('LOG_'):
            level = event.replace('LOG_','').upper()
            msg = params if isinstance(params, str) else (params.get('message') if isinstance(params, dict) else str(params))
            meta = params.get('meta') if isinstance(params, dict) else None
        elif event == 'log':
            if isinstance(params, dict):
                level = params.get('level','INFO').upper()
                msg = params.get('message','')
                meta = params.get('meta')
            else:
                msg = str(params)
                level = 'INFO'
        else:
            return

        lvl_num = getattr(log_levels, level, log_levels.INFO)
        if lvl_num < self.level:
            return

        self._write(level, msg, meta)

    def _write(self, level, message, meta):
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d %H:%M:%S')
        meta_str = ''
        if meta is not None:
            try:
                import json
                meta_str = json.dumps(meta, ensure_ascii=False)
            except Exception:
                meta_str = str(meta)

        line = self.format.replace('{date}', date_str).replace('{level}', level).replace('{message}', str(message)).replace('{meta}', meta_str)
        if self.mode == 'console':
            sys.stdout.write(line + '\n')
            sys.stdout.flush()
        else:
            os.makedirs(self.log_dir, exist_ok=True)
            file_log_name = os.path.join(self.log_dir, 'app.log')
            with open(file_log_name, 'a', encoding='utf-8') as f:
                f.write(line + '\n')


# вспомогательная функция для других модулей для emit журналов через observe_service
def emit(level, message, meta=None):
    from Src.Core.observe_service import observe_service
    payload = {'level': level, 'message': message}
    if meta is not None:
        payload['meta'] = meta
    observe_service.create_event('log', payload)
