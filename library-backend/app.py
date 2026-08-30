from flask import Flask, jsonify
from flask_cors import CORS
from extensions import db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    db.init_app(app)

    @app.route("/", methods=["GET"])
    @app.route("/api", methods=["GET"])
    def index():
        return jsonify({
            "status": "online",
            "service": "AI Library Backend API",
            "version": "1.0.0",
            "health": "/api/health",
            "endpoints": {
                "auth": "/api/auth/login",
                "books": "/api/books",
                "transactions": "/api/transactions",
                "fines": "/api/fines",
                "users": "/api/users",
                "ai": "/api/ai/recommendations/<user_id>",
                "analytics": "/api/analytics/dashboard"
            }
        }), 200

    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "message": "Library AI Backend Operating"}), 200

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "error": "Endpoint not found", "code": 404}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"success": False, "error": "Internal server error", "code": 500}), 500

    from routes.auth import auth_bp
    from routes.books import books_bp
    from routes.transactions import transactions_bp
    from routes.fines import fines_bp
    from routes.users import users_bp
    from routes.reservations import reservations_bp
    from routes.analytics import analytics_bp
    from routes.recommendations import recommendations_bp
    from routes.notifications import notifications_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(books_bp, url_prefix="/api/books")
    app.register_blueprint(transactions_bp, url_prefix="/api/transactions")
    app.register_blueprint(fines_bp, url_prefix="/api/fines")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(reservations_bp, url_prefix="/api/reservations")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
    app.register_blueprint(recommendations_bp, url_prefix="/api/ai")
    app.register_blueprint(notifications_bp, url_prefix="/api/notifications")

    with app.app_context():
        import models.user, models.book, models.transaction, models.reservation
        import models.fine, models.rating, models.notification, models.search_log
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=Config.FLASK_PORT)

