from persistence.repository import AbstractRepository
from persistence.utils import fetchall, fetchone, execute


class UserRepository(AbstractRepository):
    @staticmethod
    def find_all():
        query = '''
                SELECT `id`, `username`, `password` AS 'digest', `admin` AS 'role'
                FROM `user`
                ORDER BY `admin` DESC, `username`;
        '''

        return [User.create(data) for data in fetchall(query)]

    @staticmethod
    def find_by_id(user_id):
        query = '''
                SELECT `id`, `username`, `password` AS 'digest', `admin` AS 'role'
                FROM `user`
                WHERE `id` = %s;
        '''
        args = (user_id,)

        return User.create(fetchone(query, args))

    @staticmethod
    def find_all_by_username_like(username):
        query = '''
                SELECT `id`, `username`, `password` AS 'digest', `admin` AS 'role'
                FROM `user`
                WHERE `username` LIKE %s
                ORDER BY `admin` DESC, `username`;
        '''
        args = (f'%{username}%',)

        return [User.create(data) for data in fetchall(query, args)]

    @staticmethod
    def find_by_username(username):
        query = '''
                SELECT `id`, `username`, `password` AS 'digest', `admin` AS 'role'
                FROM `user`
                WHERE `username` = %s;
        '''
        args = (username,)

        return User.create(fetchone(query, args))

    @staticmethod
    def save(user):
        if not user.id:
            query = '''
                    INSERT INTO `user`
                        (`username`, `password`, `admin`)
                    VALUES(%s, %s, %s);
            '''
            args = (user.username, user.digest, user.admin)
            user.id = execute(query, args)
        else:
            query = '''
                    UPDATE `user`
                    SET `username` = %s,
                        `password` = %s,
                        `admin` = %s
                    WHERE `id` = %s;
            '''
            args = (user.username, user.digest, user.admin, user.id)
            execute(query, args)

        return user

    @staticmethod
    def delete_by_id(user_id):
        query = '''
                DELETE FROM `user`
                WHERE `id` = %s;
        '''
        args = (user_id,)
        execute(query, args)


from persistence.model.user import User
