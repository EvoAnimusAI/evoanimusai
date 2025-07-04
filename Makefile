.PHONY: check-spanish fix-terms tox qa

check-spanish:
	@bash scripts/check_spanish_terms.sh

fix-terms:
	@echo "🔧 Corrigiendo términos en español por sus equivalentes en inglés..."
	@find . -type f \
		-not -path "./.venv/*" \
		-not -path "./.git/*" \
		-not -name "*.md" \
		-not -name "*.po" \
		-not -name "*.txt" \
		-exec sed -i \
			-e "s/entrop[ií]a/entropy/g" \
			-e "s/acción/action/g" \
			-e "s/ruido/noise/g" \
			-e "s/estado/state/g" {} +;
	@echo "✅ Corrección automática completada."

tox:
	tox

qa:
	pre-commit run --all-files
