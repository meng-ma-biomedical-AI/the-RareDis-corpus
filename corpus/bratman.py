class Error(Exception):
    """Base class for other exceptions"""
    pass


class NotValidPath(Error):
    """Raised when the path introduced is not valid"""
    pass


def update_index(value):
    value = str(value + 1)
    value = 'T'+value
    return value


def order_brat(path):
    """
        Params:
            path: main directory path which contains brat files
        Output:
           Brat files ordered replaced in directory
    """

    try:
        import time
        import pandas as pd
        import numpy as np
        import glob
        import gc  # Garbage Collector to release unreferenced memory
        import os
        start_time = time.time()
        iteration = 0
        extension = '*.ann'
        files = glob.glob(os.path.join(path, extension))
        for file in files:
            file_path = file
            header_list = ["id", "type", "text"]
            ann_df = pd.read_csv(file_path, header=None, sep='\t', lineterminator='\n', names=header_list)
            split_df = ann_df['type'].str.replace(';', ' ').str.split(' ', expand=True)
            split_df.drop(columns=[0], inplace=True)
            split_df.fillna(value=np.nan, inplace=True)
            split_df = split_df.astype('float32')
            max_len = int(len(split_df.columns))
            char_c_number = []
            full_c_number = [i for i in range(1, max_len+1)]
            for i in range(0, int(max_len/2)):
                n = (i + 1) + (1 * i)
                char_c_number.append(n)
            result_df = pd.concat([ann_df, split_df], axis=1)
            del ann_df
            del split_df
            del header_list
            gc.collect()
            result_df.sort_values(by=char_c_number, na_position='first', inplace=True)
            result_df.reset_index(drop=True, inplace=True)
            result_df.reset_index(inplace=True)
            result_df['index'] = result_df['index'].apply(update_index)
            result_df.drop(columns=['id'], inplace=True)
            result_df.drop(columns=full_c_number, inplace=True)
            del char_c_number
            del full_c_number
            result_df.to_csv(file_path, index=False, header=False, encoding='utf-8', sep='\t', line_terminator='\n')
            del result_df
            gc.collect()
            iteration += 1
        print('Total files processed: {} '.format(iteration))
        print('Process order BRAT files is completed in time {}s'.format(time.time() - start_time))
        print('Output files saved in {}'.format(path))
    except Exception as e:
        print("Oops!", e.__class__, "occurred. Execution not performed.")


def count_entities(path, count_df=None):
    """
        Params:
            path: main directory path which contains brat files
        Output:
            File with the count of entities inside directory
    """

    try:
        import time
        import pandas as pd
        import numpy as np
        import glob
        import gc  # Garbage Collector to release unreferenced memory
        import os
        start_time = time.time()
        iteration = 0
        extension = '*.ann'
        files = glob.glob(os.path.join(path, extension))
        for file in files:
            file_path = file
            header_list = ["id", "type", "text"]
            ann_df = pd.read_csv(file_path, header=None, sep='\t', lineterminator='\n', names=header_list)
            split_df = ann_df['type'].str.replace(';', ' ').str.split(' ', expand=True).copy()
            del header_list
            del ann_df
            gc.collect()
            max_len = int(len(split_df.columns - 1))
            char_c_number = [i for i in range(1, max_len)]
            split_df.drop(columns=char_c_number, inplace=True)
            split_df.rename(columns={0: "Entities"}, inplace=True)
            split_grouped_df = split_df.groupby((['Entities'])).size().copy()
            result_df = pd.DataFrame(split_grouped_df, columns=['Number'])
            del char_c_number
            del split_df
            del split_grouped_df
            gc.collect()
            if iteration == 0:
                count_df = result_df.copy()
            else:
                count_df = pd.concat([count_df, result_df])
            del result_df
            gc.collect()
            iteration += 1
        total_df = count_df.groupby((['Entities']))['Number'].sum().copy()
        del count_df
        gc.collect()
        total_entities = total_df.sum()
        total_df.loc['TOTAL'] = total_entities
        print('Total files processed: {} '.format(iteration))
        total_df.to_csv(path + r'\1_Count_entities_output.txt', index=True, header=True, encoding='utf-8', sep='\t',
                        line_terminator='\n')
        del total_df
        gc.collect()
        print('Entities count of BRAT files is completed in time {}s'.format(time.time() - start_time))
        print('Output file saved in {}'.format(path))
    except Exception as e:
        print("Oops!", e.__class__, "occurred. Execution not performed.")


def main():
    """
        Params:
            dir_path: main directory path which contains the brat files to be ordered
        Optional Keyword Arguments:
            bratman.py
                Default. No arguments provided, replace dir_path
            bratman.py arg1
                arg1 = dir_path
            bratman.py arg1 arg2
                arg1 = '-c': count entities in brpython3 bratman.py at files
                       '-o': order brat files
                       '-co or -oc': count and order brat files
                arg2 = dir_pathpython3 bratman.py 
    """
    import sys
    import os

    if len(sys.argv) == 1:
        try:
            dir_path = r"/home/claudia/brat-v1.3_Crunchy_Frog/data/examples/gold_nlp4rare_corpus/dev/"  # Replace by desired directory path
            if not os.path.isdir(dir_path):
                raise NotValidPath
            print('Directory path used: {}'.format(dir_path))
            print('Order BRAT files? [Y/N]')
            input_order = input()
            order_brat(dir_path) if input_order == 'Y' or input_order == 'y' else print('Execution not performed.')
            print('Count entities inside BRAT files? [Y/N]')
            input_order = input()
            count_entities(dir_path) if input_order == 'Y' or input_order == 'y' else print('Execution not performed.')
            print('Process finished. Goodbye!')
        except NotValidPath:
            print("Directory path introduced is not valid!! Please, introduce a valid path.")

    if len(sys.argv) == 2:
        try:
            dir_path = sys.argv[1]
            if not os.path.isdir(dir_path):
                raise NotValidPath
            print('Directory path used: {}'.format(dir_path))
            print('Order BRAT files? [Y/N]')
            input_order = input()
            order_brat(dir_path) if input_order == 'Y' or input_order == 'y' else print('Execution not performed.')
            print('Count entities inside BRAT files? [Y/N]')
            input_order = input()
            count_entities(dir_path) if input_order == 'Y' or input_order == 'y' else print('Execution not performed.')
            print('Process finished. Goodbye!')
        except NotValidPath:
            print("Directory path introduced is not valid!! Please, introduce a valid path.")

    if len(sys.argv) > 2:
        try:
            dir_path = sys.argv[2]
            if not os.path.isdir(dir_path):
                raise NotValidPath
            print('Directory path used: {}'.format(dir_path))
            if sys.argv[1] == '-o':
                order_brat(dir_path)
            elif sys.argv[1] == '-c':
                count_entities(dir_path)
            elif sys.argv[1] == '-co' or sys.argv[1] == '-oc':
                order_brat(dir_path)
                count_entities(dir_path)
            else:
                print('Not valid arguments provided. Check instructions.')
            print('Process finished. Goodbye!')
        except NotValidPath:
            print("Directory path introduced is not valid!! Please, introduce a valid path.")


if __name__ == "__main__":
    main()
