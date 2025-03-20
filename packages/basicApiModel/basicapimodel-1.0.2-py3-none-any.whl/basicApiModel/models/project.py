import os
import shutil
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class Project:
    """
        Class to initialize a new API project based on a predefined template.
    """

    def __init__(self):
        raise Exception("This class should not be instantiated")

    @classmethod
    def __install_requirements(cls, requirements_path):
        """
            Installs the packages listed in requirements.txt.
        """
        try:
            subprocess.run(
                ["pip", "install", "-r", requirements_path],
                check=True
            )
            logging.info("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            logging.error("⚠ Error installing dependencies.")

    @classmethod
    def create(cls, destination="."):
        """
            Copies the template files to the target directory.
        """
        package_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
        template_dir = os.path.join(package_dir, "template")

        if not os.path.exists(template_dir):
            logging.error("❌ Error: 'template' folder not found.")
            return

        for item in os.listdir(template_dir):
            src = os.path.join(template_dir, item)
            dst = os.path.join(destination, item)

            if os.path.exists(dst):
                logging.warning("[!] Warning: %s already exists. Skipping...",
                                dst)
                continue

            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)

        logging.info("✅ Project created successfully! 🚀")

        # Check if requirements.txt exists and ask the
        # user if they want to install dependencies
        requirements_path = os.path.join(destination, "requirements.txt")
        if os.path.exists(requirements_path):
            logging.warning(
                "  ⚠ IMPORTANT: Before installing dependencies, "
                "ensure your virtual environment is active!"
            )
            logging.warning("   If you haven't created one, "
                            "use these commands:")
            logging.warning("   Windows: python -m venv venv && "
                            "venv\\Scripts\\activate")
            logging.warning(
                "   Linux/macOS: python3 -m venv venv && source "
                "venv/bin/activate\n"
            )

            response = input(
                "📦 Do you want to install the packages from requirements.txt?"
                " (y/n): "
            ).strip().lower()
            if response in ["y", "yes"]:
                cls.__install_requirements(requirements_path)
            else:
                logging.info(
                    "\n🚀 Project is ready! Don't forget to install "
                    "dependencies later:"
                )
                logging.info("   pip install -r requirements.txt")
