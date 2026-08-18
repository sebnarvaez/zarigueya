from zari.zari_model import ProjectConfig, TemplateConfig

projectConfig = ProjectConfig(
    root = "templates",
    templates = [
            TemplateConfig(
                item = "app/cmd/web/handlers.mako.go",
                copymode = "once"
            ),
            TemplateConfig(
                item = "app/internal/views/model_admin.mako.templ",
                oname = "${name}_admin.templ",
                copymode = "per_model"

            ),
            TemplateConfig(
                item = "app/internal/views/model_display.mako.templ",
                oname = "${name}_display.templ",
                copymode = "per_model"

            ),
            TemplateConfig(
                item = "app/internal/views/model_ui_builder.mako.go",
                oname = "${name}_ui_builder.go",
                copymode = "per_model"
            ),
            TemplateConfig(
                item = "app/models/model.mako.go",
                oname = "${name}_model.go",
                copymode = "per_model"
            )
    ]
)