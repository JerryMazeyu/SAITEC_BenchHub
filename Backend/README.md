## 1. Initialize Database

```
$env:FLASK_APP = "run.py"  // Make sure environment variable
flask db init  		   // Initialize the database
flask db migrate -m "Initial migration"  // Migration database
flask db upgrade           // Upgrade database
```





![1735535400314](image/README/1735535400314.png)
