from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    def on_start(self):
        """Se ejecuta al inicio de la prueba. Aquí realizamos el login y accedemos automáticamente al perfil."""
        self.login()

    @task(1)
    def index(self):
        """Simula un usuario accediendo a la página principal"""
        self.client.get("/")

    @task(2)
    def dashboard(self):
        """Simula un usuario accediendo al dashboard"""
        self.client.get("/dashboard")

    @task(3)
    def register_incident(self):
        """Simula un usuario registrando una incidencia"""
        self.client.post("/register_incident", data={
            "project": "Test Project",
            "description": "Test Description",
            "position": "Test Position",
            "responsible": "Test Responsible",
            "status": "Abierto"
        })

    @task(4)
    def kpis(self):
        """Simula un usuario viendo los KPIs"""
        self.client.get("/kpis")

    @task(5)
    def logout(self):
        """Simula un usuario cerrando sesión"""
        self.client.get("/logout")

    def login(self):
        """Simula un usuario iniciando sesión y automáticamente accediendo al perfil"""
        response = self.client.post("/login", data={
            "email": "test@example.com",
            "password": "Password123!"
        })
        if response.status_code == 200:
            # Después de iniciar sesión, el usuario es redirigido a /profile
            self.client.get("/profile")

    @task(6)
    def register(self):
        """Simula un usuario registrándose"""
        self.client.post("/register", data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "NewPassword123!",
            "confirm_password": "NewPassword123!"
        })

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # Espera entre 1 y 5 segundos entre tareas
    host = "http://127.0.0.1:5000"  # Especifica el host base aquí

if __name__ == "__main__":
    import os
    os.system("locust -f test_performance.py")
