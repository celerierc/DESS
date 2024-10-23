
def get_expected_file_split_stats(df_master, df_c, df_r):
    print(f"+{'-'*20}+")
    print(f"| Total    : {len(df_master):<5}  |")
    print(f"| Complete : {len(df_c):<5}  |")
    print(f"| Reprocess: {len(df_r):<5}   |")
    print(f"|{'-'*20}|")
    print(f"| ToDo     : {len(df_master) - (len(df_c)+len(df_r)):<5}   |")
    print(f"+{'-'*20}+")