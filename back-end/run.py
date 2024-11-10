from app import create_app
from controllers import search_items



if __name__ == '__main__':
    app = create_app(init=True)
    # with app.app_context():
    #     print("searching")
    #     search_items('显示器')  
    app.run(debug=True)
