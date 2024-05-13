    # # Fetch data from Neo4j
    # users_df, listings_df, reviews_df = neo4j_manager.fetch_user_listing_data()

    # # Generate positive and negative samples
    # existing_links_df = reviews_df
    # existing_links_df['label'] = 1  # Positive examples
    
    # # Generate negative samples by selecting non-links
    # all_users = list(users_df['user_id'])
    # all_listings = list(listings_df['listing_id'])
    
    # random_pairs = [(random.choice(all_users), random.choice(all_listings)) for _ in range(1000)]
    # negative_samples = [pair for pair in random_pairs if pair not in existing_links_df[['user_id', 'listing_id']].values.tolist()]
    
    # negative_examples_df = pd.DataFrame(negative_samples, columns=['user_id', 'listing_id'])
    # negative_examples_df['label'] = 0  # Negative examples
    
    # # Combine positive and negative examples
    # training_data_df = pd.concat([existing_links_df, negative_examples_df], ignore_index=True)

    # # Fetch FastRP embeddings for Listings
    # fastrp_df = neo4j_manager.fetch_fastrp_embeddings()
    
    # # Merge embeddings with training data
    # for i in range(16):  # Adjust based on embeddingDimension
    #     training_data_df[f'embed_{i}'] = fastrp_df['embedding'].apply(lambda x: x[i] if x else None)
    
    # # Train link prediction model
    # clf = neo4j_manager.train_link_prediction_model(training_data_df)

    # # Example: Recommend listings for a specific user
    # user_id = 'some_user_id'  # Replace with an actual user ID
    # recommendations = neo4j_manager.recommend_listings(user_id, clf, all_listings, training_data_df)

    # print("Recommendations for User", user_id)
    # print(recommendations)