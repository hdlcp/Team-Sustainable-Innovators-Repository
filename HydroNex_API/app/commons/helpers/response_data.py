
class ResponseData:
    @staticmethod
    def login(user,access_token):
        """
        Structure les données de la réponse pour la connexion d'un utilisateur.
        """
        return {
            "user": user.to_dict(),
            "access_token": access_token
        }
  
    @staticmethod
    def get_all_user(users_data, page, per_page, current_page, sort_direction, sort_field, q, total_pages, total):
        return{
            'users_data': users_data,
            'page': page,
            'per_page': per_page,
            "current_page": current_page,
            'sort_direction': sort_direction,
            'sort_field':sort_field,
            "q":q,
            'total_pages': total_pages,
            'total':total
        }
        
    @staticmethod
    def get_all_badge(badges_data, page, per_page, current_page, sort_direction, sort_field, q, total_pages, total):
        return{
            'badges_data': badges_data,
            'page': page,
            'per_page': per_page,
            "current_page": current_page,
            'sort_direction': sort_direction,
            'sort_field':sort_field,
            "q":q,
            'total_pages': total_pages,
            'total':total
        }
        
    @staticmethod
    def get_all_formation(formations_data, page, per_page, current_page, sort_direction, sort_field, q, total_pages, total):
        return{
            'formations_data': formations_data,
            'page': page,
            'per_page': per_page,
            "current_page": current_page,
            'sort_direction': sort_direction,
            'sort_field':sort_field,
            "q":q,
            'total_pages': total_pages,
            'total':total
        }
        
    @staticmethod
    def get_all_module_formation(modules_formations_data, page, per_page, current_page, sort_direction, sort_field, q, total_pages, total):
        return{
            'modules_formations_data': modules_formations_data,
            'page': page,
            'per_page': per_page,
            "current_page": current_page,
            'sort_direction': sort_direction,
            'sort_field':sort_field,
            "q":q,
            'total_pages': total_pages,
            'total':total
        }