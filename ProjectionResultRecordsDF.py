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
            # iter through second left axis
            for j in range(input_shape[j_axis_idx]):
                filtered_rows = resultRecordsDF[(resultRecordsDF[i_axis_name] == i) & (resultRecordsDF[j_axis_name] == j)]
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


    def set_z_as_flat_axis(self, resultRecordsDF, flataxis):
        ax_lvl_names = ["x_idx", "y_idx", "z_idx"]
        flat_axis_name = ax_lvl_names.pop(flataxis)
        outputDF = resultRecordsDF.rename(columns={ax_lvl_names[0]: "x_idx", ax_lvl_names[1]: "y_idx", flat_axis_name: "z_idx"})
        return outputDF