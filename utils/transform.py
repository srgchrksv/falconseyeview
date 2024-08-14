def sort_df(df, sort_col, col='userRatingCount'):
    return (
        df[["id", "rating", col, "types"]]
        .sort_values(by=sort_col, ascending=False)
        .reset_index(drop=True)
    )