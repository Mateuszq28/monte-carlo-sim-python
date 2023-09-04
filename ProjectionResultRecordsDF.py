from ColorPointDF import ColorPointDF
import pandas as pd

class ProjectionResultRecordsDF():
    def __init__(self):
        pass

    def x_high(self, resultRecordsDF, input_shape, sum_axis=False, sort=True, reset_colors=None, connect_lines=None):
        return self.throw(resultRecordsDF, input_shape, 0, -1, sum_axis=sum_axis, sort=sort, reset_colors=reset_colors, connect_lines=connect_lines)

    def x_low(self, resultRecordsDF, input_shape, sum_axis=False, sort=True, reset_colors=None, connect_lines=None):
        return self.throw(resultRecordsDF, input_shape, 0, 1, sum_axis=sum_axis, sort=sort, reset_colors=reset_colors, connect_lines=connect_lines)

    def y_high(self, resultRecordsDF, input_shape, sum_axis=False, sort=True, reset_colors=None, connect_lines=None):
        return self.throw(resultRecordsDF, input_shape, 1, -1, sum_axis=sum_axis, sort=sort, reset_colors=reset_colors, connect_lines=connect_lines)

    def y_low(self, resultRecordsDF, input_shape, sum_axis=False, sort=True, reset_colors=None, connect_lines=None):
        return self.throw(resultRecordsDF, input_shape, 1, 1, sum_axis=sum_axis, sort=sort, reset_colors=reset_colors, connect_lines=connect_lines)

    def z_high(self, resultRecordsDF, input_shape, sum_axis=False, sort=True, reset_colors=None, connect_lines=None):
        return self.throw(resultRecordsDF, input_shape, 2, -1, sum_axis=sum_axis, sort=sort, reset_colors=reset_colors, connect_lines=connect_lines)

    def z_low(self, resultRecordsDF, input_shape, sum_axis=False, sort=True, reset_colors=None, connect_lines=None):
        return self.throw(resultRecordsDF, input_shape, 2, 1, sum_axis=sum_axis, sort=sort, reset_colors=reset_colors, connect_lines=connect_lines)

    def throw(self, resultRecordsDF: pd.DataFrame, input_shape, axis, xray, sum_axis=False, sort=True, reset_colors=None, connect_lines=None):
        """
        The function will take first value from object3D.body (recovered from resultRecordsDF) seen perpendicularly to axis.
        :param axis: observer's axis
        :param xray: If 1, observer is looking at the body from the start of the axis (axis[0]). If -1, observer is looking at the body from the end of the axis (axis[-1]).
        """
        ax_lvl_list = [0,1,2]
        ax_lvl_names = ["x_idx", "y_idx", "z_idx"]
        ax_lvl_list.remove(axis)
        ax_lvl_names_active = ax_lvl_names.copy()
        search_axis_name = ax_lvl_names_active.pop(axis)
        resultRecordsDF_copy = resultRecordsDF.copy()
        # sum projection DF
        if sum_axis:
            ColorPointDF.sum_same_idx(df = resultRecordsDF_copy,
                                      subset = ax_lvl_names_active)
        # NEW FASTER METHOD FOR SCANNING
        # find first or last val on the search axis
        if xray == -1:
            # find last value on search axis
            finded_idx = resultRecordsDF_copy.groupby(by=ax_lvl_names_active, as_index=False, sort=False, dropna=False)[search_axis_name].max()[search_axis_name]
        elif xray == 1:
            # find first value on search axis
            finded_idx = resultRecordsDF_copy.groupby(by=ax_lvl_names_active, as_index=False, sort=False, dropna=False)[search_axis_name].min()[search_axis_name]
        else:
            raise ValueError("xray must be -1 or 1")
        # finded_idx has one column (search_axis_name)
        # (localization of the finded values to keep)
        # drop duplicates to achieve the same lenth as finded_idx (groupby)
        # when keep="first":
            # it will return value that was added to the records earlier
            # (lower index in resultRecords, index 0 of list with finded values)
        resultRecordsDF_copy.drop_duplicates(subset=ax_lvl_names_active, inplace=True, ignore_index=True, keep="first")
        resultRecordsDF_copy[search_axis_name] = finded_idx
        output_df = resultRecordsDF_copy
        # OLD SLOW METHOD - ITERATION
        """
        # prepare for scanning values
        i_axis_idx = ax_lvl_list[0]
        j_axis_idx = ax_lvl_list[1]
        i_axis_name = ax_lvl_names[i_axis_idx]
        j_axis_name = ax_lvl_names[j_axis_idx]
        output_df = pd.DataFrame()
        # iter through first left axis
        # for example if x_high -> axis=0:
        #   i iters through y axis and j inters through z axis
        for i in range(input_shape[i_axis_idx]):
            filtered_rows_candidates = resultRecordsDF_copy[resultRecordsDF_copy[i_axis_name] == i]
            # iter through second left axis
            for j in range(input_shape[j_axis_idx]):
                filtered_rows = filtered_rows_candidates[filtered_rows_candidates[j_axis_name] == j]
                if len(filtered_rows) > 0:
                    # find first or last val on the search axis
                    # if there are more then one finded values it will return value that was added to the records earlier (lower index, index 0 of list with finded values)
                    if xray == -1:
                        # observer is at the end of the axis, so we are looking for the last (max idx) value
                        first_val = filtered_rows.loc[[filtered_rows[search_axis_name].idxmax()]]
                    elif xray == 1:
                        # observer is at the beginning of the axis, so we are looking for the first (min idx) value
                        first_val = filtered_rows.loc[[filtered_rows[search_axis_name].idxmin()]]
                    else:
                        raise ValueError("xray must be -1 or 1")
                    # here add to output container
                    output_df = pd.concat([output_df, first_val], ignore_index=True)
        """
        # reset idx on search value axis (we want flat 3d object)
        if xray == -1:
            reset_idx = input_shape[axis] -1
        elif xray == 1:
            reset_idx = 0
        else:
            raise ValueError("xray must be -1 or 1")
        output_df[search_axis_name] = reset_idx
        # [make arrows flat] reset idx on search value axis (we want flat 3d object)
        if connect_lines is not None:
            proj_connect_lines = connect_lines.copy()
            arrow_cols_1 = ["x_idx", "y_idx", "z_idx"]
            arrow_cols_2 = ["x_idx_2", "y_idx_2", "z_idx_2"]
            arrow_reset_col_1 = arrow_cols_1.pop(axis)
            arrow_reset_col_2 = arrow_cols_2.pop(axis)
            proj_connect_lines[arrow_reset_col_1] = reset_idx
            proj_connect_lines[arrow_reset_col_2] = reset_idx
        else:
            proj_connect_lines = None
        # we will need flat axis idx to change 3d object to 2d array later
        # (all idx values on flat axis column are the same)
        flat_axis = axis
        # sort output to have same colors like in propEnv processing
        if sort:
            output_df.sort_values(["x_idx", "y_idx", "z_idx"], ignore_index=True, inplace=True)
        if reset_colors is not None:
            output_df = ColorPointDF().reset_colors(output_df, reset_colors)
        return output_df, flat_axis, proj_connect_lines


    def set_z_as_flat_axis(self, resultRecordsDF, flataxis, input_shape, post_transform=True, transform_preset=None, sort=True, reset_colors=None, connect_lines=None):
        ax_lvl_names = ["x_idx", "y_idx", "z_idx"]
        flat_axis_name = ax_lvl_names.pop(flataxis)
        outputDF = resultRecordsDF.rename(columns={ax_lvl_names[0]: "x_idx", ax_lvl_names[1]: "y_idx", flat_axis_name: "z_idx"})
        # make flat z connect_lines arrows
        if connect_lines is not None:
            arrow_cols_1 = ["x_idx", "y_idx", "z_idx"]
            arrow_cols_2 = ["x_idx_2", "y_idx_2", "z_idx_2"]
            arrow_reset_col_1 = arrow_cols_1.pop(flataxis)
            arrow_reset_col_2 = arrow_cols_2.pop(flataxis)
            flat_z_connect_lines = connect_lines.rename(columns={arrow_cols_1[0]: "x_idx", arrow_cols_1[1]: "y_idx", arrow_reset_col_1: "z_idx", arrow_cols_2[0]: "x_idx_1", arrow_cols_2[1]: "y_idx_2", arrow_reset_col_2: "z_idx_2"})
        else:
            flat_z_connect_lines = None
        # rotate and inverse axis if need
        image_shape = input_shape.copy()
        image_shape.pop(flataxis)
        if post_transform:
            if transform_preset is not None and input_shape is not None:
                # on print image arrow of y axis is directed upwards (not down like in standard image)
                if transform_preset == "x_high":
                    self.rotate_left(outputDF, image_shape)
                    if flat_z_connect_lines is not None:
                        self.rotate_left(flat_z_connect_lines, image_shape)
                elif transform_preset == "x_low":
                    self.rotate_left(outputDF, image_shape)
                    self.inverese_vertical(outputDF, image_shape)
                    if flat_z_connect_lines is not None:
                        self.rotate_left(flat_z_connect_lines, image_shape)
                        self.inverese_vertical(flat_z_connect_lines, image_shape)
                elif transform_preset == "y_high":
                    self.rotate_left(outputDF, image_shape)
                    self.inverese_vertical(outputDF, image_shape)
                    if flat_z_connect_lines is not None:
                        self.rotate_left(flat_z_connect_lines, image_shape)
                        self.inverese_vertical(flat_z_connect_lines, image_shape)
                elif transform_preset == "y_low":
                    self.rotate_left(outputDF, image_shape)
                    if flat_z_connect_lines is not None:
                        self.rotate_left(flat_z_connect_lines, image_shape)
                elif transform_preset == "z_high":
                    pass
                elif transform_preset == "z_low":
                    self.inverese_horizontal(outputDF, image_shape)
                    if flat_z_connect_lines is not None:
                        self.inverese_horizontal(flat_z_connect_lines, image_shape)
                else:
                    raise ValueError("transform_preset not recognized")
            else:
                raise ValueError("To do post_transform input_shape and transform_preset are needed.")
        # sort output to have same colors like in propEnv processing
        if sort:
            outputDF.sort_values(["x_idx", "y_idx", "z_idx"], ignore_index=True, inplace=True)
        if reset_colors is not None:
            outputDF = ColorPointDF().reset_colors(outputDF, reset_colors)
        return outputDF, image_shape, flat_z_connect_lines
    

    def rotate_left(self, df: pd.DataFrame, image_shape):
        self.flip_axis(df, ax1=0, ax2=1, image_shape=image_shape)
        self.inverese_horizontal(df, image_shape=image_shape)

    def rotate_right(self, df: pd.DataFrame, image_shape):
        self.flip_axis(df, ax1=0, ax2=1, image_shape=image_shape)
        self.inverese_vertical(df, image_shape=image_shape)

    def inverese_vertical(self, df: pd.DataFrame, image_shape):
        df["y_idx"] = image_shape[1] - 1 - df["y_idx"]
        # for connect lines arrows
        if "y_idx_2" in df.columns:
            df["y_idx_2"] = image_shape[1] - 1 - df["y_idx_2"]

    def inverese_horizontal(self, df: pd.DataFrame, image_shape):
        df["x_idx"] = image_shape[0] - 1 - df["x_idx"]
        # for connect lines arrows
        if "x_idx_2" in df.columns:
            df["x_idx_2"] = image_shape[0] - 1 - df["x_idx_2"]

    def flip_axis(self, df: pd.DataFrame, ax1, ax2, image_shape):
        axis_names = ["x_idx", "y_idx", "z_idx"]
        ax1_name = axis_names[ax1]
        ax2_name = axis_names[ax2]
        df.rename(columns={ax1_name: ax2_name, ax2_name: ax1_name}, inplace=True)
        # for connect lines arrows
        if "x_idx_2" in df.columns or "y_idx_2" in df.columns or "z_idx_2" in df.columns:
            axis_names = ["x_idx_2", "y_idx_2", "z_idx_2"]
            ax1_name = axis_names[ax1]
            ax2_name = axis_names[ax2]
            df.rename(columns={ax1_name: ax2_name, ax2_name: ax1_name}, inplace=True)
        # change image shape list
        bufor = image_shape[ax1]
        image_shape[ax1] = image_shape[ax2]
        image_shape[ax2] = bufor