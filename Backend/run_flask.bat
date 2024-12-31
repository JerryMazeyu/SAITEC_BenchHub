@echo off
REM Flask 批处理脚本
REM 支持 dev/test 环境启动、数据库重置和初始化

REM 设置默认环境变量
SET FLASK_APP=manage.py
SET FLASK_ENV=development

REM 检查传入的第一个参数
IF "%1"=="run" (
    REM 启动应用
    IF "%2"=="dev" (
        SET FLASK_ENV=development
        echo Starting Flask in development environment...
    ) ELSE IF "%2"=="test" (
        SET FLASK_ENV=testing
        echo Starting Flask in testing environment...
    ) ELSE (
        echo Invalid environment! Use "dev" or "test".
        EXIT /B 1
    )
    flask run
    EXIT /B 0
)

IF "%1"=="db_reset" (
    REM 重置数据库：删除、创建、迁移并更新
    echo Resetting the database...
    flask db downgrade
    flask db upgrade
    echo Database reset complete.
    EXIT /B 0
)

IF "%1"=="db_init" (
    REM 初始化数据库并运行 scripts 目录中的脚本
    SET CONFIG=%2
    IF "%CONFIG%"=="" (
        SET CONFIG=app.config.DevelopmentConfig
    )
    echo Initializing database with config: %CONFIG%...
    flask db init || echo Migration environment already exists.
    flask db migrate
    flask db upgrade
    echo Running scripts in /scripts...
    FOR %%f IN (scripts\*.py) DO (
        python %%f
        echo Executed script: %%f
    )
    echo Database initialization complete.
    EXIT /B 0
)

REM 显示帮助信息
echo Usage: run_flask.bat [command] [options]
echo Commands:
echo   run [dev|test]         Start Flask in development or testing environment.
echo   db_reset               Reset the database (drop and recreate).
echo   db_init [config]       Initialize the database and run scripts (default: development config).
EXIT /B 0
