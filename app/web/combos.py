from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.web import web_bp
from app.extensions import db
from app.models.combo import Combo, ComboItem
from app.models.product import Product
from sqlalchemy.exc import IntegrityError
import uuid


@web_bp.route("/combos", methods=["GET"])
@login_required
def combos_list():
    combos = Combo.query.all()
    return render_template("admin/combos/list.html", combos=combos)


@web_bp.route("/combos/new", methods=["GET", "POST"])
@login_required
def combos_create():
    if request.method == "POST":
        data = request.get_json()
        items_data = data.pop("items", [])
        
        try:
            # Pegamos o canteen_id do primeiro produto ou do usuário se for injetado
            # Por enquanto, como é admin simplificado, vamos pegar de canteen_id se presente ou do primeiro produto
            canteen_id = data.get("canteen_id")
            if not canteen_id and items_data:
                p = db.session.get(Product, items_data[0]["product_id"])
                canteen_id = p.canteen_id
            
            new_combo = Combo(
                code=data.get("code"),
                name=data.get("name"),
                short_name=data.get("short_name"),
                price_type=data.get("price_type", "auto_sum"),
                custom_price=data.get("custom_price"),
                image_url=data.get("image_url"),
                status=data.get("status", True),
                canteen_id=canteen_id
            )
            
            for item in items_data:
                combo_item = ComboItem(
                    product_id=uuid.UUID(item["product_id"]),
                    quantity=item.get("quantity", 1)
                )
                new_combo.items.append(combo_item)

            db.session.add(new_combo)
            db.session.commit()
            return jsonify({"message": "Combo criado com sucesso!", "id": str(new_combo.id)}), 201
            
        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "Código de combo já existente"}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": str(e)}), 500

    products = Product.query.filter_by(status=True).all()
    return render_template("admin/combos/form.html", combo=None, products=products)


@web_bp.route("/combos/<uuid:combo_id>/edit", methods=["GET", "PUT"])
@login_required
def combos_edit(combo_id):
    combo = db.session.get(Combo, combo_id)
    if not combo:
        if request.method == "PUT":
            return jsonify({"message": "Combo não encontrado"}), 404
        flash("Combo não encontrado.", "danger")
        return redirect(url_for("web.combos_list"))

    if request.method == "PUT":
        data = request.get_json()
        items_data = data.pop("items", None)
        
        try:
            combo.code = data.get("code", combo.code)
            combo.name = data.get("name", combo.name)
            combo.short_name = data.get("short_name", combo.short_name)
            combo.price_type = data.get("price_type", combo.price_type)
            combo.custom_price = data.get("custom_price") if data.get("price_type") == "custom" else None
            combo.image_url = data.get("image_url", combo.image_url)
            combo.status = data.get("status", combo.status)
            
            if items_data is not None:
                # Remove itens antigos
                for old_item in combo.items[:]:
                    db.session.delete(old_item)
                combo.items = []
                
                # Adiciona novos
                for item in items_data:
                    combo_item = ComboItem(
                        product_id=uuid.UUID(item["product_id"]),
                        quantity=item.get("quantity", 1)
                    )
                    combo.items.append(combo_item)
            
            db.session.commit()
            return jsonify({"message": "Combo atualizado com sucesso!"}), 200
            
        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "Código de combo já existente"}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": str(e)}), 500

    products = Product.query.filter_by(status=True).all()
    return render_template("admin/combos/form.html", combo=combo, products=products)


@web_bp.route("/combos/<uuid:combo_id>", methods=["DELETE"])
@login_required
def combos_delete(combo_id):
    combo = db.session.get(Combo, combo_id)
    if not combo:
        return jsonify({"message": "Combo não encontrado"}), 404
        
    try:
        db.session.delete(combo)
        db.session.commit()
        return "", 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
