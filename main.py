from drivers import fb_driver

if __name__ == '__main__':
    message = "Hello World!"
    fb_driver.post_text(message)
