from Src.Core.abstract_dto import abstract_dto

# Модель рецепта (dto)
# Пример
#        "name":"ВАФЛИ ХРУСТЯЩИЕ В ВАФЕЛЬНИЦЕ",
#        "composition":[
#            {
#                "nomenclature_id":"0c101a7e-5934-4155-83a6-d2c388fcc11a",
#                "range_id":"adb7510f-687d-428f-a697-26e53d3f65b7",
#                "value":100
#            }
#        ],
#        "portions":10,
#        "cooking_time":"20 мин",
#        "steps":[
#            "Как испечь вафли хрустящие в вафельнице? Подготовьте необходимые продукты. Из данного количества у меня получилось 8 штук диаметром около 10 см.",
#            "Масло положите в сотейник с толстым дном. Растопите его на маленьком огне на плите, на водяной бане либо в микроволновке.",
#            "Добавьте в теплое масло сахар. Перемешайте венчиком до полного растворения сахара. От тепла сахар довольно быстро растает.",
#            "Добавьте в масло яйцо. Предварительно все-таки проверьте масло, не горячее ли оно, иначе яйцо может свариться. Перемешайте яйцо с маслом до однородности.",
#            "Всыпьте муку, добавьте ванилин.",
#            "Перемешайте массу венчиком до состояния гладкого однородного теста.",
#            "Разогрейте вафельницу по инструкции к ней. У меня очень старая, еще советских времен электровафельница. Она может и не очень красивая, но печет замечательно! Я не смазываю вафельницу маслом, в тесте достаточно жира, да и к ней уже давно ничего не прилипает. Но вы смотрите по своей модели. Выкладывайте тесто по столовой ложке. Можно класть немного меньше теста, тогда вафли будут меньше и их получится больше.",
#            "Пеките вафли несколько минут до золотистого цвета. Осторожно откройте вафельницу, она очень горячая! Снимите вафлю лопаткой. Горячая она очень мягкая, как блинчик."
#        ]
class receipt_dto(abstract_dto):
    __composition:list = []
    __portions:float = 0
    __cooking_time:str = ""
    __steps:list = []


    # Количество порций
    @property
    def portions(self) -> float:
        return self.__portions
    
    @portions.setter
    def portions(self, value:float):
        self.__portions = value


    # Время приготовления
    @property
    def cooking_time(self) -> str:
        return self.__cooking_time
    
    @cooking_time.setter
    def cooking_time(self, value:str):
        self.__cooking_time = value

    # Шаги приготовления
    @property
    def steps(self) -> list:
        return self.__steps
    
    @steps.setter
    def steps(self, value):
        self.__steps = value
    
    # Состав
    @property
    def composition(self) -> list:
        return self.__composition
    
    @composition.setter
    def composition(self, value):
        self.__composition = value

