from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from .sub import SubApp


class MainApp:
    def __init__(
        self,
        application_title: str,
        applications: list[tuple[str, SubApp]],
        startups: list[callable] = None,
        shutdowns: list[callable] = None,
        version: str = "*",
        redirection_path: str = None,
        redoc_url: str | None = None,
        docs_url: str | None = None,
        allow_credentials: bool = False,
        allow_methods: list[str] | None = None,
        allow_headers: list[str] | None = None,
        allow_origins: list[str] | None = None,
    ):
        """
        Initialize a MainApp instance and create the FastAPI application.
        """
        self.application_title = application_title
        self.applications = applications
        self.version = version
        self.redirection_path = redirection_path
        self.redoc_url = redoc_url
        self.docs_url = docs_url
        self.allow_credentials = allow_credentials
        self.startups = startups or []
        self.shutdowns = shutdowns or []
        self.allow_methods = allow_methods or ["*"]
        self.allow_headers = allow_headers or ["*"]
        self.allow_origins = allow_origins or ["*"]
        self.app = self._create_app()

    def _create_app(self) -> FastAPI:
        """
        Create and configure the FastAPI application.
        """

        # Default redirection path
        if self.redirection_path is None and self.applications:
            self.redirection_path = self.applications[0][0]

        # Initialize FastAPI app
        app = FastAPI(
            title=self.application_title,
            version=self.version,
            redoc_url=self.redoc_url,
            docs_url=self.docs_url,
            swagger_ui_parameters={"defaultModelsExpandDepth": -1},
        )

        # Startup event handlers
        @app.on_event("startup")
        async def startup():
            for startup_application in self.startups:
                startup_application()

        # Shutdown event handlers
        @app.on_event("shutdown")
        async def shutdown_event():
            for shutdown_application in self.shutdowns:
                shutdown_application()

        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_credentials=self.allow_credentials,
            allow_methods=self.allow_methods,
            allow_headers=self.allow_headers,
            allow_origins=self.allow_origins,
        )

        # Mount sub-applications
        for path, application in self.applications:
            app.mount(path, application.get_app())

        # Redirect root to the specified path
        if self.redirection_path:
            @app.get("/", status_code=302)
            async def redirect():
                return RedirectResponse(self.redirection_path)

        return app

    def get_app(self) -> FastAPI:
        """
        Get the created FastAPI application instance.
        """
        return self.app
