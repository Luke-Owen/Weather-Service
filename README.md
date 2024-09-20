Weather app that show the forecast of whatever city you like using Visual Crossing's API. 
Written in Python using Django framework and a React frontend.

Steps to use:

1. Clone repository.
2. Using terminal or cmd on the root dir of your project, Run `pip install -r requirements.txt`, to install packages and dependencies.
3. If migrations haven't been run, go to manage.py in the terminal tab, run `makemigrations`, then `migrate`.
4. Create a `.env` file and add your Django app secret and Visual Crossing API key that can get from signing up on their [website](https://www.visualcrossing.com/)
5. Install [redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/) on your local machine and make sure it is running. 
6. Launch project from your chosen IDE, I'm using PyCharm. Remember to edit you launch config to point launch url to `http://localhost:8000/Core`
