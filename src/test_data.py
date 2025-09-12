"""Test campaigns with sample keywords."""

"""
Test data was generated with OpenAI gpt-4.1 model with the following prompt:

You're a campaign manager specialist that sets up campaigns in Google Ads.

<objective>
Generate a list of keywords describing a real ad campaign set in Google Ads.
</objective>

<rules>
- keywords are generated per campaign
- there should be 5 campaigns
- each campaign should have between 5 and 30 keywords
- campaigns should vary, both with the theme and the number of keywords
- keywords describe what the specific campaign advertise (e.g. some product)
- in most cases keyword shouldn't be long phrase, max 4 words
- the output must be in english
- your response must have a JSON format specified in <output_format>
</rules>

<output_format>
[
	{
		"campaign_name": <campaign name>
		"description": <short description about campaign, what does it advertise>
		"keywords": <list of keywords>
	}
]
</output_format>
"""


TEST_DATA = [
    {
        "campaign_name": "Premium Laptops Sale",
        "description": "This campaign advertises premium and latest model laptops for technology enthusiasts and professionals.",
        "keywords": [
            "buy laptops",
            "premium laptops",
            "best laptops",
            "new laptops",
            "high performance laptops",
            "gaming laptops",
            "ultrabooks",
            "laptop deals",
            "laptop online",
            "business laptops",
        ],
    },
    {
        "campaign_name": "Organic Skincare Products",
        "description": "This campaign promotes organic, chemical-free skincare products targeting health-conscious customers.",
        "keywords": [
            "organic skincare",
            "natural face cream",
            "organic moisturizer",
            "chemical free skincare",
            "herbal face mask",
            "natural body lotion",
            "vegan skincare",
            "eco friendly cosmetics",
            "organic sunscreen",
        ],
    },
    {
        "campaign_name": "Home Fitness Equipment",
        "description": "This campaign advertises a range of fitness equipment for home workouts.",
        "keywords": [
            "home gym equipment",
            "buy treadmill",
            "workout dumbbells",
            "resistance bands",
            "fitness equipment online",
            "exercise bike",
            "pull up bar",
            "yoga mats",
            "fitness accessories",
        ],
    },
    {
        "campaign_name": "Pet Food and Accessories",
        "description": "This campaign promotes high-quality pet food, toys, and accessories for dogs and cats.",
        "keywords": [
            "dog food",
            "cat food",
            "pet toys",
            "pet accessories",
            "healthy pet treats",
            "dog collars",
            "cat litter",
            "pet grooming",
            "pet supplies online",
            "pet beds",
        ],
    },
    {
        "campaign_name": "Custom T-Shirt Printing",
        "description": "This campaign advertises custom t-shirt printing services for events and personal use.",
        "keywords": [
            "custom t shirts",
            "t shirt printing",
            "personalized shirts",
            "print your design",
            "event t shirts",
            "company t shirts",
            "design your shirt",
            "bulk t shirt printing",
            "custom apparel",
        ],
    },
    {
        "campaign_name": "Premium Noise Cancelling Headphones",
        "description": "Advertising the latest wireless noise-cancelling headphones for audiophiles and tech enthusiasts.",
        "keywords": [
            "wireless headphones",
            "noise cancelling",
            "Bluetooth headphones",
            "over ear headphones",
            "best headphones",
            "music headphones",
            "headphone deals",
            "active noise cancelling",
            "premium headphones",
            "headphone sale",
        ],
    },
    {
        "campaign_name": "Organic Skincare Essentials",
        "description": "Promoting a range of natural and organic skincare products for all skin types.",
        "keywords": [
            "organic skincare",
            "natural face cream",
            "herbal moisturizer",
            "eco friendly skincare",
            "vegan beauty products",
            "cruelty free lotion",
            "best organic face wash",
            "natural serum",
            "plant based skincare",
            "organic body butter",
            "skincare for sensitive skin",
        ],
    },
    {
        "campaign_name": "Digital Marketing Online Courses",
        "description": "Targeting professionals interested in learning digital marketing skills through online courses.",
        "keywords": [
            "digital marketing course",
            "SEO training",
            "learn Google Ads",
            "social media marketing",
            "online marketing classes",
            "PPC course",
            "content marketing course",
            "email marketing training",
            "marketing certification online",
            "internet marketing course",
        ],
    },
    {
        "campaign_name": "EcoSmart Home Appliances",
        "description": "Showcasing energy efficient and environmentally friendly home appliances.",
        "keywords": [
            "energy efficient fridge",
            "eco smart washing machine",
            "low energy dishwasher",
            "green home appliances",
            "smart thermostat",
            "solar water heater",
            "appliance energy rating",
            "environmentally friendly oven",
            "sustainable appliances",
        ],
    },
    {
        "campaign_name": "Summer Adventure Travel Packages",
        "description": "Promoting all-inclusive summer travel and adventure packages for families and thrill seekers.",
        "keywords": [
            "summer travel deals",
            "adventure vacation",
            "family holiday package",
            "beach getaway",
            "all inclusive travel",
            "rafting trips",
            "guided hiking tours",
            "adventure travel 2024",
            "outdoor adventure holiday",
            "summer flight deals",
            "travel package discounts",
            "vacation tours",
        ],
    },
    {
        "campaign_name": "Eco-Friendly Kitchen Products",
        "description": "Promotes sustainable and environmentally-friendly kitchenware such as bamboo utensils, reusable food wraps, and compostable dish sponges.",
        "keywords": [
            "eco kitchenware",
            "bamboo utensils",
            "sustainable kitchen",
            "compostable sponges",
            "reusable food wraps",
            "green cookware",
            "zero waste kitchen",
            "environmentally friendly utensils",
            "plastic free kitchen",
        ],
    },
    {
        "campaign_name": "Online Coding Bootcamp",
        "description": "Advertises a virtual coding bootcamp offering intensive programming courses in web development, data science, and app development.",
        "keywords": [
            "coding bootcamp",
            "learn programming",
            "web development course",
            "online coding classes",
            "data science bootcamp",
            "python classes",
            "java programming",
            "front end development",
            "full stack bootcamp",
            "javascript course",
            "app development course",
            "virtual coding bootcamp",
            "software engineering course",
        ],
    },
    {
        "campaign_name": "Luxury Dog Beds",
        "description": "Showcases high-end, comfortable, and stylish dog beds for pet owners seeking premium products for their dogs.",
        "keywords": [
            "luxury dog beds",
            "premium dog bed",
            "orthopedic pet bed",
            "stylish dog beds",
            "best dog beds",
            "memory foam dog bed",
        ],
    },
]
