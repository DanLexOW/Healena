from aiogram.types import BotCommand

private = {
    BotCommand(command="start", description="Давайте начнем"),
    BotCommand(command="menu", description="меню"),
    BotCommand(command="enter_meal_statistics", description="Введите продукты с граммовкой и соотношением БЖУ, входящие в ваш прием пищи"),
    BotCommand(command="report", description="Узнайте вашу 'калорийную' статистику за сегодня"),
    BotCommand(command="finish_stat", description="Прекратить отправку калорийной статистики")
}
