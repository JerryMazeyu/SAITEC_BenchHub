@echo off
:: 定义 Flask 应用入口
set FLASK_APP=run.py

:: 检查参数
if "%1" == "dev" (
    echo Running Flask in Development Environment...
    set FLASK_ENV=development
    set FLASK_CONFIG=app.config.DevelopmentConfig
    flask run
) else if "%1" == "test" (
    echo Running Flask in Testing Environment...
    set FLASK_ENV=testing
    set FLASK_CONFIG=app.config.TestingConfig
    flask run
) else (
    echo Usage: run_flask.bat {dev|test}
    echo    dev  - Run Flask in development mode
    echo    test - Run Flask in testing mode
)
