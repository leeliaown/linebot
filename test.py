def leave(keyword):

    time = re.findall(r"\d{1,2}", keyword[2])

    period = re.findall(r"\b\w{1,2}\b", keyword[2])

    if len(time) > 2:

        for k, v in leaves.items():

            if k in keyword[3] and "上午" in keyword[2]:

                flex_msg = [
                    keyword[1][4:],
                    leaves[k],
                    time[0]+"/"+time[1],
                    time[2]+"/"+time[3],
                    "上午",
                ]

            elif k in keyword[3] and "下午" in keyword[2]:

                flex_msg = [
                    keyword[1][4:],
                    leaves[k],
                    time[0]+"/"+time[1],
                    time[2]+"/"+time[3],
                    "下午",
                ]

            else:
                for k, v in leaves.items():

                    if k in keyword[4]:

                        flex_msg = [
                            keyword[1][4:],
                            leaves[k],
                            time[0]+"/"+time[1],
                            time[2]+"/"+time[3],
                            "",
                        ]

                    else:

                        flex_msg = [
                            keyword[1][4:],
                            leaves[k],
                            time[0]+"/"+time[1],
                            time[2]+"/"+time[3],
                            "",
                        ]

    else:

        for k, v in leaves.items():

            if k in keyword[3] and "上午" in keyword[2]:

                flex_msg = [
                    keyword[1][4:],
                    leaves[k],
                    time[0]+"/"+time[1],
                    time[0]+"/"+time[1],
                    "上午",
                ]

            elif k in keyword[3] and "下午" in keyword[2]:

                flex_msg = [
                    keyword[1][4:],
                    leaves[k],
                    time[0]+"/"+time[1],
                    time[0]+"/"+time[1],
                    "下午",
                ]

            elif k in keyword[3]:

                flex_msg = [
                    keyword[1][4:],
                    leaves[k],
                    time[0]+"/"+time[1],
                    time[0]+"/"+time[1],
                    "",

                ]

        # if "上午" in keyword[2]:

        #     flex_msg = [
        #         keyword[1][4:],
        #         keyword[3][-3:],
        #         time[0]+"/"+time[1],
        #         time[0]+"/"+time[1],
        #         "上午",
        #     ]

        # elif "下午" and "病假回診" in keyword[3]:

        #     flex_msg = [
        #         keyword[1][4:],
        #         "病假",
        #         time[0]+"/"+time[1],
        #         time[0]+"/"+time[1],
        #         "下午",
        #     ]

        # elif "下午" in keyword[2]:

        #     flex_msg = [
        #         keyword[1][4:],
        #         keyword[3][-3:],
        #         time[0]+"/"+time[1],
        #         time[0]+"/"+time[1],
        #         "下午",
        #     ]

        # else:

        #     if "：" in keyword[3][-3:] or ":" in keyword[3][-3:]:

        #         flex_msg = [
        #             keyword[1][4:],
        #             keyword[3][-2:],
        #             time[0]+"/"+time[1],
        #             time[0]+"/"+time[1],
        #             "",
        #         ]

        #     elif "。" and "特休假" in keyword[3]:

        #         a = keyword[3].strip("。")

        #         flex_msg = [
        #             keyword[1][4:],
        #             a[-3:-1],
        #             time[0]+"/"+time[1],
        #             time[0]+"/"+time[1],
        #             "",
        #         ]

            # else:

            #     flex_msg = [
            #         keyword[1][4:],
            #         keyword[3][-3:],
            #         time[0]+"/"+time[1],
            #         time[0]+"/"+time[1],
            #         "",
            #     ]
    return flex_msg
