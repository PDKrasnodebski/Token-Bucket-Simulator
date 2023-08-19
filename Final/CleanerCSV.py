import csv
import os


class CleanerCSV:

    def clean(*id_list: int):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        relative_path = os.path.join(current_dir,"logs","csv")

        paths = dict()

        for id in id_list:

            paths.update({id: os.path.join(current_dir,"logs","txt",f"logs_{id}.txt")})
        
        for id, filepath in paths.items():
                try:
                    with open(filepath, 'r') as file:
                        lines = file.readlines()
                    tokens = []
                    for line in lines:
                        if 'Tokens:' in line:
                            token_value = line.split(':')[1].split()[0]
                            tokens.append(token_value)

                    with open(f'{relative_path}\logs_{id}.csv', 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Tokens'])
                        writer.writerows([[token] for token in tokens])
                except Exception as e:
                    print("Error occured, could not convert file to logs", str(e))   

if __name__=="__main__":
        

    id_list = []
    if id_list:

        current_dir = os.path.dirname(os.path.abspath(__file__))
        relative_path = os.path.join(current_dir,"logs","csv")

        for filename in os.listdir(f'{current_dir}/logs/txt/'):
            try:
                check_if_was_used = filename.split(".")[0][5:]
                check_if_was_used = int(check_if_was_used)
                if check_if_was_used in id_list:
                    it_was = True
            except:
                it_was = False
                pass

            if filename.endswith('.txt') and not filename.endswith('.gitkeep') and it_was:
                try:
                    with open(f'{current_dir}/logs/txt/{filename}', 'r') as file:
                        lines = file.readlines()
                    tokens = []
                    for line in lines:
                        if 'Tokens:' in line:
                            token_value = line.split(':')[1].split()[0]
                            tokens.append(token_value)

                    with open(f'{relative_path}\cleaned_{check_if_was_used}.csv', 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Tokens'])
                        writer.writerows([[token] for token in tokens])
                except Exception as e:
                    print("Error occured, could not convert file to logs", str(e))

