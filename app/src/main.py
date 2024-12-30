from pyftpdlib.handlers import TLS_FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer
from app.utils.logger import logger
from app.config.configuration import ApiConfiguration
ftp_secret = ApiConfiguration().ftp_secret

class FTPServerHandler(TLS_FTPHandler):

    def on_connect(self):
        logger.info(f'FTP Server Connected {self.remote_ip}, {self.remote_port}')

    def on_disconnect(self):
        logger.info(f'{self.remote_ip} disconnected')

    def on_login(self, username):
        logger.info(f'Username {username} logged in')

    def on_logout(self, username):
        logger.info(f'Username {username} logged out')

    def on_file_sent(self, file):
        logger.info(f'File Downloaded {file}')

    def on_file_received(self, file):
        logger.info(f'File Uploaded {file}')

    def on_incomplete_file_sent(self, file):
        logger.info(f'Incomplete {file} sent')

    def on_incomplete_file_received(self, file):
        logger.info(f'Incomplete file downloaded')
        import os
        os.remove(file)

def main():
    authorizer = DummyAuthorizer()
    authorizer.add_user(ftp_secret.username, ftp_secret.password, ftp_secret.homedir, perm='elradfmwMT')
    authorizer.add_anonymous(ftp_secret.homedir)

    handler = FTPServerHandler
    handler.certfile = ftp_secret.ssl_certificate
    handler.keyfile =  ftp_secret.ssl_certificate_key
    handler.tls_control_required = True
    handler.tls_data_required = True
    handler.authorizer = authorizer
    server = FTPServer((ftp_secret.host, ftp_secret.port), handler)
    server.serve_forever()

if __name__ == '__main__':
    main()