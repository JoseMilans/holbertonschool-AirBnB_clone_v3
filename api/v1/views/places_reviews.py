#!/usr/bin/python3
"""
Module: places_reviews.py
Contains views for handling RESTFul API actions related to Review objects.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage, Place, Review, User

@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews_by_place(place_id):
    """
    Retrieves the list of all Review objects of a given Place.
    Returns:
        JSON: List of reviews associated with the Place.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a specific Review object based on its ID.
    ew_id (str): The ID of the Review to retrieve.

    Returns:
        JSON: Details of the specified Review.
    """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)

@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object based on its ID.
    Returns:
        JSON: Empty dictionary with a status code of 200 upon successful deletion.
    """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    abort(404)

@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
    Creates a new Review object associated with a Place.
    Returns:
        JSON: Details of the newly created Review with a status code of 201.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    if 'text' not in data:
        abort(400, "Missing text")

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    data['place_id'] = place_id
    new_review = Review(**data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201

@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates an existing Review object based on its ID.

    Args:
        review_id (str): The ID of the Review to update.

    Returns:
        JSON: Details of the updated Review with a status code of 200.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200