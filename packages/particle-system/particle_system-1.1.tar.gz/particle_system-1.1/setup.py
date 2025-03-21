from setuptools import setup, find_packages


setup(name='particle_system',
      version=1.1, 
      author="At7791",
      author_email="a@a.com",
      description="Easy to use visual Particle System for pygame Games",
      packages=find_packages(),
      include_package_data=True,
      package_data={'particle_system': ["default_particles/arrow.png","default_particles/circle.png","default_particles/heart.png","default_particles/lightning.png","default_particles/pentagone.png","default_particles/square.png","default_particles/star.png"]},
      install_requires=["pygame"],
      license="MIT",
      long_description="For more informations you can visit the github repository. https://github.com/At7791/Particle-System",
      )