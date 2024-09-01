from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    def on_start(self):
        """Se ejecuta al inicio de la prueba. Realiza el registro de usuario."""
        self.register()

    def register(self):
        """Simula un usuario registrándose."""
        response = self.client.post("/register", data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "NewPassword123!",
            "confirm_password": "NewPassword123!"
        })
        if response.status_code == 200:
            # Después de registrarse, el usuario es redirigido a /profile
            self.client.get("/profile")
            # Navega al index después del perfil
            self.index()

    def login(self):
        """Simula un usuario iniciando sesión con las credenciales del último registro."""
        response = self.client.post("/login", data={
            "email": "newuser@example.com",
            "password": "NewPassword123!"
        })
        if response.status_code == 200:
            # Después de iniciar sesión, el usuario es redirigido a /profile
            self.client.get("/profile")
            # Navega al index después del perfil
            self.index()

    @task(1)
    def index(self):
        """Simula un usuario accediendo a la página principal."""
        self.client.get("/")
        # Continuar con la secuencia hacia el registro de incidencia
        self.register_incident()

    @task(2)
    def register_incident(self):
        """Simula un usuario registrando una incidencia."""
        response = self.client.post("/register_incident", data={
            "project": "Test Project",
            "description": "Test Description",
            "position": "Test Position",
            "responsible": "Test Responsible",
            "status": "Abierto"
        })
        if response.status_code == 200:
            self.dashboard()

    @task(3)
    def dashboard(self):
        """Simula un usuario accediendo al dashboard y filtrando por proyecto."""
        response = self.client.get("/dashboard")
        if response.status_code == 200:
            self.client.get("/dashboard?project=Test+Project")
            self.kpis()

    @task(4)
    def kpis(self):
        """Simula un usuario viendo los KPIs."""
        response = self.client.get("/kpis")
        if response.status_code == 200:
            self.logout()

    @task(5)
    def logout(self):
        """Simula un usuario cerrando sesión."""
        self.client.get("/logout")
        # Realiza una nueva autenticación después del logout
        self.login()

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # Espera entre 1 y 5 segundos entre tareas
    host = "http://127.0.0.1:5000"  # Especifica el host base aquí

if __name__ == "__main__":
    import os
    os.system("locust -f test_performance.py")
