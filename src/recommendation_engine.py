def generate_recommendations(segment):
    """
    Generate customer-specific recommendations
    based on the predicted customer segment.
    """

    recommendations = {
        "Premium": {
            "strategy": "Retain and reward high-value customers",
            "recommendations": [
                "Offer exclusive premium products and personalized deals.",
                "Provide loyalty rewards and early access to new products.",
                "Use targeted offers to increase purchase frequency."
            ]
        },

        "Regular": {
            "strategy": "Increase customer value through upselling and engagement",
            "recommendations": [
                "Recommend product bundles and complementary products.",
                "Provide personalized discounts to encourage higher spending.",
                "Introduce loyalty programs to increase customer retention."
            ]
        },

        "Budget": {
            "strategy": "Increase engagement and encourage conversion",
            "recommendations": [
                "Offer affordable products and value-for-money deals.",
                "Use discounts and promotional campaigns to increase purchases.",
                "Recommend products based on previous purchasing behavior."
            ]
        }
    }

    return recommendations.get(
        segment,
        {
            "strategy": "General customer engagement",
            "recommendations": [
                "Provide personalized product recommendations."
            ]
        }
    )