import os
from setuptools import setup


setup(name="endless-fake",
      version="0.1.0",
      description="Playing Endless Lake with Machine Learning",
      long_description=open(
          os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")
      ).read(),
      long_description_content_type="text/markdown",
      classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
      ],
      keywords="machinelearning ai artificialintelligence game videogame",
      url="https://github.com/aisouard/endless-fake",
      project_urls={
          "Source": "https://github.com/aisouard/endless-fake/",
          "Tracker": "https://github.com/aisouard/endless-fake/issues",
      },
      author="Axel Isouard",
      author_email="axel@isouard.fr",
      license="MIT",
      packages=["endless_fake"],
      install_requires=[
          "markdown",
      ],
      test_suite="nose.collector",
      tests_require=["nose"],
      entry_points={
          "console_scripts": [
              "endless-fake=endless_fake.command_line:main",
              "endless-fake-evaluate=endless_fake.command_line.evaluate:main",
              "endless-fake-fetch=endless_fake.command_line.fetch:main",
              "endless-fake-genetics=endless_fake.command_line.genetics:main",
              "endless-fake-patch=endless_fake.command_line.patch:main",
              "endless-fake-playback=endless_fake.command_line.playback:main",
              "endless-fake-record=endless_fake.command_line.record:main",
              "endless-fake-restore=endless_fake.command_line.restore:main",
              "endless-fake-teach=endless_fake.command_line.teach:main",
              "endless-fake-train=endless_fake.command_line.train:main",
          ],
      },
      include_package_data=True,
      zip_safe=False)
