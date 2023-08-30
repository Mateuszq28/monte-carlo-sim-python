from ColorPointDF import ColorPointDF
import pandas as pd

class ProjectionResultRecordsDF():
    def __init__(self):
        pass

    def x_high(self, resultRecordsDF, input_shape):
        return self.throw(resultRecordsDF, input_shape, 0, -1)

    def x_low(self, resultRecordsDF, input_shape):
        return self.throw(resultRecordsDF, input_shape, 0, 1)

    def y_high(self, resultRecordsDF, input_shape):
        return self.throw(resultRecordsDF, input_shape, 1, -1)

    def y_low(self, resultRecordsDF, input_shape):
        return self.throw(resultRecordsDF, input_shape, 1, 1)

    def z_high(self, resultRecordsDF, input_shape):
        return self.throw(resultRecordsDF, input_shape, 2, -1)

    def z_low(self, resultRecordsDF, input_shape):
        return self.throw(resultRecordsDF, input_shape, 2, 1)

    def throw(self, resultRecordsDF: pd.DataFrame, input_shape, axis, xray):
        """
        The function will take first value from object3D.body (recovered from resultRecordsDF) seen perpendicularly to axis.
        :param axis: observer's axis
        :param xray: If 1, observer is looking at the body from the start of the axis (axis[0]). If -1, observer is looking at the body from the end of the axis (axis[-1]).
        """
        ax_lvl_list = [0,1,2]
        ax_lvl_names = ["x_idx", "y_idx", "z_idx"]
        ax_lvl_list.remove(axis)
        # iter through first left axis
        # for example if x_high -> axis=0:
        #   i iters through y axis and j inters through z axis
        i_axis_idx = ax_lvl_list[0]
        j_axis_idx = ax_lvl_list[1]
        i_axis_name = ax_lvl_names[i_axis_idx]
        j_axis_name = ax_lvl_names[j_axis_idx]
        search_axis_name = ax_lvl_names[axis]
        output_df = pd.DataFrame()
        for i in range(input_shape[i_axis_idx]):
            filtered_rows_candidates = resultRecordsDF[resultRecordsDF[i_axis_name] == i]
            # iter through second left axis
            for j in range(input_shape[j_axis_idx]):
                filtered_rows = filtered_rows_candidates[filtered_rows_candidates[j_axis_name] == j]
                if len(filtered_rows) > 0:
                    # find first or last val on the search axis
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
        # reset idx on search value axis (we want flat 3d object)
        if xray == -1:
            reset_idx = input_shape[axis] -1
        elif xray == 1:
            reset_idx = 0
        else:
            raise ValueError("xray must be -1 or 1")
        output_df[search_axis_name] = reset_idx
        # we will need flat axis idx to change 3d object to 2d array later
        # (all idx values on flat axis column are the same)
        flat_axis = axis
        return output_df, flat_axis


    def set_z_as_flat_axis(self, resultRecordsDF, flataxis, post_transform=True, transform_preset=None, input_shape=None):
        ax_lvl_names = ["x_idx", "y_idx", "z_idx"]
        flat_axis_name = ax_lvl_names.pop(flataxis)
        outputDF = resultRecordsDF.rename(columns={ax_lvl_names[0]: "x_idx", ax_lvl_names[1]: "y_idx", flat_axis_name: "z_idx"})
        # rotate and inverse axis if need
        if post_transform:
            if transform_preset is not None and input_shape is not None:
                input_shape = input_shape.copy()
                input_shape.pop(flataxis)
                if transform_preset == "x_high":
                    self.rotate_left(outputDF, input_shape)
                elif transform_preset == "x_low":
                    self.rotate_left(outputDF, input_shape)
                    self.inverese_vertical(outputDF, input_shape)
                elif transform_preset == "y_high":
                    self.rotate_left(outputDF, input_shape)
                    self.inverese_vertical(outputDF, input_shape)
                elif transform_preset == "y_low":
                    self.rotate_left(outputDF, input_shape)
                elif transform_preset == "z_high":
                    pass
                elif transform_preset == "z_low":
                    self.inverese_horizontal(outputDF, input_shape)
                else:
                    raise ValueError("transform_preset not recognized")
            else:
                raise ValueError("To do post_transform input_shape and transform_preset are needed.")
        return outputDF
    

    def rotate_left(self, df: pd.DataFrame, input_shape):
        self.flip_axis(df, ax1=0, ax2=1)
        self.inverese_horizontal(df, input_shape)

    def rotate_right(self, df: pd.DataFrame, input_shape):
        self.flip_axis(df, ax1=0, ax2=1)
        self.inverese_vertical(df, input_shape)

    def inverese_vertical(self, df: pd.DataFrame, input_shape):
        df["y_idx"] = input_shape[1] - 1 - df["y_idx"]

    def inverese_horizontal(self, df: pd.DataFrame, input_shape):
        df["x_idx"] = input_shape[0] - 1 - df["x_idx"]

    def flip_axis(self, df: pd.DataFrame, ax1, ax2):
        axis_names = ["x_idx", "y_idx", "z_idx"]
        ax1_name = axis_names[ax1]
        ax2_name = axis_names[ax2]
        df.rename(columns={ax1_name: ax2_name, ax2_name: ax1_name})