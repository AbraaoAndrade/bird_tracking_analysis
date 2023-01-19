import streamlit as st
import numpy as np
import pandas as pd
import tqdm as tq
from datetime import datetime,timedelta
from colorama import Fore, Back
import glob 
import os
import tqdm.notebook as tq

class preprocess_tracking:

    def __init__(self, path, animal):

        self.path = path 
        self.animal = animal
        
    def strtomonth(self, mes):
      if mes == "Jan":  monthNUM = 1;
      elif mes == "Feb":  monthNUM = 2;
      elif mes == "Mar":  monthNUM = 3;
      elif mes == "Apr":  monthNUM = 4;
      elif mes == "May":  monthNUM = 5;
      elif mes == "Jun":  monthNUM = 6;
      elif mes == "Jul":  monthNUM = 7;
      elif mes == "Aug":  monthNUM = 8;
      elif mes == "Sep":  monthNUM = 9;
      elif mes == "Oct": monthNUM = 10;
      elif mes == "Nov": monthNUM = 11;
      elif mes == "Dec": monthNUM = 12;
      else: print('invalid');
      return monthNUM

    # A. Generating the list of directories that will be read to account for the distance traveled
    def load_files(self, return_results=False, print_results=False):
        list_folders = sorted(glob.glob(self.path + "/*/"))

        list_filenames = np.array([])
        for folder in tq.tqdm(list_folders):
            filenames = glob.glob(os.path.join(folder, "*.csv"))

            list_filenames = np.hstack([list_filenames, filenames])

        self.list_filenames = sorted(list_filenames)
        
        if print_results:
            print("\n".join(self.list_filenames))
            
        if return_results:
            return self.list_filenames

    # B. Checking light
    def get_light(self, return_results=False, print_results=False):
        # 0 declarando variavies -------------------------------------------------------------------------------------------
        coord = np.array([])
        luz = True
        self.light_on = []

        for k,j in enumerate(tq.tqdm(self.list_filenames)): ## for geral que irá caminhar por cada filename

            # 1 lendo filename ---------------------------------------------------------------------------------------------
            filename = j
            dataSet = pd.read_csv(filename,names = ['a','b','c','d','e','f','g']) ## lendo filename
            dataSet_np = np.array(dataSet) ## transformando em numpy array para ganhar velocidade de processamento
            # --------------------------------------------------------------------------------------------------------------

            # 2 separando os dados de tempo e coordenada -------------------------------------------------------------------
            timet = dataSet_np[:,4:] 
            coord = dataSet_np[:,1:3]
            # --------------------------------------------------------------------------------------------------------------

            for i in range(len(timet)): ## for que irá caminhar por cada linha da tabela lida

                # 3 extraindo os dados de tempo ----------------------------------------------------------------------------
                ano = int(filename[len(filename)-17:len(filename)-13])
                mes = int(self.strtomonth(filename[len(filename)-21:len(filename)-18]))
                dia = int(filename[len(filename)-24:len(filename)-22])
                hora = int(timet[i,0])
                minu = int(timet[i,1])
                seg = int(timet[i,2])
                mics = int(100*(dataSet_np[i,6]%1))
                # ---------------------------------------------------------------------------------------------------------- 

                # 4 checando ligar/desligar da luz -------------------------------------------------------------------------
                if coord[i,0] == 160.5 and coord[i,1] == 120.5 and luz == True:
                    if print_results:
                        print(Back.BLACK + Fore.WHITE + " OFF →", datetime(ano,mes,dia,hora,minu,seg), "", filename, "")
                    luz = False

                elif coord[i,0] != 160.5 and coord[i,1] != 120.5 and luz == False:
                    if print_results:
                        print(Back.WHITE + Fore.BLACK + " ON  →", datetime(ano,mes,dia,hora,minu,seg), "", filename, "")

                    self.light_on.append(datetime(ano,mes,dia,hora,minu,seg,mics))
                    luz = True
                # ----------------------------------------------------------------------------------------------------------
  
        if return_results:
            return self.light_on

    # C. Distance calculator
    def get_distance(self, interval, filtering_mask=pd.DataFrame([]), print_results=True):

        # 0 declarando variavies --------------------------------------------------------------------------------------------
        interval = timedelta(minutes=int(interval[3:]), hours=int(interval[:2]))

        quinze_horas = datetime(2019,8,14,21,0,0) - datetime(2019,8,14,6,0,0,0)

        coord = np.array([])
        dist_cont = 0
        dist_interval = []
        times_axis = []
        dia_check = 0 
        mes_check = 0
        first_loop = True
        begin = False
        on = 0
        timefill = 0

        count_geral = 0
        # -------------------------------------------------------------------------------------------------------------------

        for k,j in enumerate(tq.tqdm(self.list_filenames)): ## for geral que irá caminhar por cada filename

            # 1 lendo filename ----------------------------------------------------------------------------------------------
            filename = j
            dataSet = pd.read_csv(filename,names = ['a','b','c','d','e','f','g']) ## lendo filename
                # 1.1 resolvendo problemas ==================================================================================
                # Problema: quando o tracking não encontra o animal ele registra a coordenada como (0,0). Assim,  
                # não podemos calcular essa falsa distancia percorrida;
                # Resolução: se a coordenada for zero mantemos a = b até q o tracking volte a funcionar (coordenada 
                # deixa de ser 0), quando b receberá a nova coordenada real ignorando todo o periodo zerado
            dataSet = dataSet.loc[~(dataSet[['b','c']]==0).all(axis=1)] 
                # ===========================================================================================================
            dataSet_np = np.array(dataSet) ## transformando em numpy array para ganhar velocidade de processamento
            # ---------------------------------------------------------------------------------------------------------------


            # 2 separando os dados de tempo e coordenada --------------------------------------------------------------------
            timet = dataSet_np[:,4:] 
            dT = dataSet_np[:,3] 
            coord = dataSet_np[:,1:3]
            # ---------------------------------------------------------------------------------------------------------------


            for i in range(len(timet)): ## for que irá caminhar por cada linha da tabela lida

                # 3 extraindo os dados de tempo -----------------------------------------------------------------------------
                ano = int(filename[len(filename)-17:len(filename)-13])
                mes = int(self.strtomonth(filename[len(filename)-21:len(filename)-18]))
                dia = int(filename[len(filename)-24:len(filename)-22])
                hora = int(timet[i,0])
                minu = int(timet[i,1])
                seg = int(timet[i,2])
                mics = int(100*(dataSet_np[i,6]%1))
                # -----------------------------------------------------------------------------------------------------------


                # 4 Identificando arquivos com problemas --------------------------------------------------------------------
                time3_check = datetime(ano,mes,dia,hora,minu,seg,mics)
                dois_minutos = datetime(2019,8,14,12,2,0,0) - datetime(2019,8,14,12,0,0,0)
                um_dia = datetime(2019,8,15,12,0,0,0) - datetime(2019,8,14,12,0,0,0)
                if begin == True:
                    if print_results:
                        if (time3_check - time2) > dois_minutos and (time3_check - time2) < um_dia:
                            print(Style.RESET_ALL + '-----------------------------------------------------')
                            print('talvez tenhamos um problema no arquivo: ', filename)
                            print('')
                            if (time3_check - time2) > dois_minutos:
                                print('O tempo de atualização de coordenadas foi mt alto:', time3_check - time2)
                            print('')
                            print('tempo de atualização: t =', time2,';t+1 = ', time3_check)
                            print('-----------------------------------------------------')
                # -----------------------------------------------------------------------------------------------------------


                # 5 resolvendo problemas ====================================================================================
                # PROBLEMA : quando temos arquivos q começam em um dia e terminam no outro as primeiras linhas receberão er-
                # roneamente os dados de dia e mês do dia seguinte; 
                # OBS.: os dados de ano, mes e dia são retirados do nome do arquivo que são nomeados com a data do final do
                # intervalo de registro (17 minutos).

                if dia_check != dia:
                    if hora == 23:
                        dia = dia_check
                    else:
                        dia_check = dia

                if mes_check != mes:
                    if hora == 23:
                        mes = mes_check
                    else:
                        mes_check = mes
                # ==========================================================================================================
                if on < len(self.light_on):
                    if datetime(ano,mes,dia,hora,minu,seg,mics) >= self.light_on[on]: ## checando a hora inicial (light on) 


                        # 6 preenchendo variaveis no primeiro loop -------------------------------------------------------------
                        if begin == False: 
                            # 6.1 preenchendo os pontos vetoriais --------------------------------------------------------------
                            b = coord[i,:]
                            a = coord[i,:]

                            # 6.2 preenchendo os datetime ----------------------------------------------------------------------  
                            if print_results:
                                print(Back.BLACK + Fore.WHITE + "==================== dia {} ====================".format(on+1))
                                print(Back.WHITE + Fore.BLACK + "         light on → {}        ".format(datetime(ano,mes,dia,hora,minu,seg)))
                            time1 = datetime(ano,mes,dia,hora,minu,seg,mics)
                            dia_check = dia
                            mes_check = mes
                            begin = True
                        # ------------------------------------------------------------------------------------------------------


                        if begin == True: ## pós o primeiro loop


                            # 7 preenchendo os pontos vetoriais -----------------------------------------------------------------
                            a = b
                            b = coord[i,:]

                            if not filtering_mask.empty:
                                # 7.1 resolvendo problemas =======================================================================
                                    # PROBLEMA: quando o tracking não encontra o animal e tem alguma mancha no contraste ele registra a
                                    # coordenada da mancha e não podemos calcular essa falsa distancia percorrida;
                                    # RESOLUÇÃO: se a coordenada corresponder aos pontos marcados na filtragem a nova coordenada é ignorada,
                                    # portanto, "b" recebe "a" para que essa distancia n seja contabilizada.
                                    # INCONSISTENCIAS:

                                if filtering_mask.loc[count_geral, "mask"]: 
                                    b = a
                                # =================================================================================================
                            #------------------------------------------------------------------------------------------------------


                            # 8 preenchendo os datetime ---------------------------------------------------------------------------
                            time2 = datetime(ano,mes,dia,hora,minu,seg,mics)
                            #------------------------------------------------------------------------------------------------------


                            # 9 calculando a distancia percorrida -----------------------------------------------------------------
                            vecR = b-a                                   
                            dist_cont += np.sqrt(sum(np.power(vecR,2))) 
                            # -----------------------------------------------------------------------------------------------------


                            # 10 gerando tabela de distancia por intervalo --------------------------------------------------------
                            if time2 - time1 >= interval: 
                                if ((time2.minute == self.light_on[on].minute) or (time2.minute == (self.light_on[on] + interval).minute)) and \
                                   (round((time2 - time1).total_seconds()/60) <= round(interval.total_seconds()/60)):
                                    if print_results:
                                        print(Back.GREEN + Fore.WHITE + " ✔ " + Style.RESET_ALL, datetime(ano,mes,dia,hora,minu,seg), int(dist_cont))
                                else:
                                    if print_results:
                                        print(Back.RED + Fore.WHITE + " ✖ " + Style.RESET_ALL, datetime(ano,mes,dia,hora,minu,seg), int(dist_cont))

                                dist_interval.append(dist_cont)

                                time1 = time2
                                times_axis.append(time1)
                                dist_cont = 0
                            # ----------------------------------------------------------------------------------------------------- 

                            if time2 - self.light_on[on] >= quinze_horas:
                                begin = False
                                dist_cont = 0

                                # 11 preenchendo os zeros da noite ----------------------------------------------------------------
                                timefill = time2
                                for fill in range(19):
                                    dist_interval.append(0)                        
                                    times_axis.append(timefill)
                                    
                                    if print_results:
                                        print(Back.WHITE + Fore.BLACK + " ▣ " + Style.RESET_ALL, timefill.replace(microsecond=0), 0)


                                    timefill = timefill + interval
                                # -------------------------------------------------------------------------------------------------

                                on += 1

                count_geral += 1


        dist_interval_df = pd.DataFrame(np.stack([times_axis, dist_interval], axis = 1), columns = ["time", "dist"])
        
        return dist_interval_df
    
    def concat_all_files(self):
        coord_total = []
        timet_total = []
        for idx, filename in enumerate(tq.tqdm(self.list_filenames)):
            dataSet = pd.read_csv(filename,names = ['a','b','c','d','e','f','g']) 
            # filtering [0,0] coords
            dataSet = dataSet.loc[~(dataSet[['b','c']]==0).all(axis=1)]
            dataSet_np = np.array(dataSet) 

            coord = dataSet_np[:,1:3]
            timet = dataSet_np[:,3] 

            if idx == 0:
                coord_total = coord
                timet_total = timet
            else:
                coord_total = np.concatenate([coord_total, coord], axis = 0)
                timet_total = np.concatenate([timet_total, timet], axis = 0)

        return coord_total, timet_total

class tracking_analysis:

    def __init__(self):

        self.path = None
        self.filter_file = pd.DataFrame([])
        self.uploaded_files = None
        self.list_filenames = None 
        self.animal = None
        self.progress_bar = None
        self.light_on = None # [datetime(2019, 9, 28, 5, 48, 4, 10), datetime(2019, 9, 29, 5, 48, 5, 82), datetime(2019, 9, 30, 5, 47, 48, 53), datetime(2019, 10, 1, 5, 47, 59, 49), datetime(2019, 10, 2, 5, 47, 46, 7), datetime(2019, 10, 3, 5, 47, 56, 95)]
        self.dataSet_all = pd.DataFrame([])
        self.label_dict = {}

    def strtomonth(self, mes):
        if mes == "Jan":  monthNUM = 1;
        elif mes == "Feb":  monthNUM = 2;
        elif mes == "Mar":  monthNUM = 3;
        elif mes == "Apr":  monthNUM = 4;
        elif mes == "May":  monthNUM = 5;
        elif mes == "Jun":  monthNUM = 6;
        elif mes == "Jul":  monthNUM = 7;
        elif mes == "Aug":  monthNUM = 8;
        elif mes == "Sep":  monthNUM = 9;
        elif mes == "Oct": monthNUM = 10;
        elif mes == "Nov": monthNUM = 11;
        elif mes == "Dec": monthNUM = 12;
        else: print('invalid');
        return monthNUM

    def get_dir_list(self):

        if st.session_state.checkbox_web_app:

            files_list = []
            
            for i, file in enumerate(self.uploaded_files):
                ano = int(file.name[len(file.name)-17:len(file.name)-13])
                mes = int(self.strtomonth(file.name[len(file.name)-21:len(file.name)-18]))
                dia = int(file.name[len(file.name)-24:len(file.name)-22])
                hora = datetime.strptime(file.name[len(file.name)-12:len(file.name)-4], "%H_%M_%S").time()

                files_list.append([ano, mes, dia, hora, file])
        
                self.progress_bar.progress((i+1)/len(self.uploaded_files))

            files_df = pd.DataFrame(files_list, columns=["year", "month", "day", "hour", "uploaded_file"])

            self.animal = file.name[-30:-25]
            self.list_filenames = list(files_df.sort_values(["year", "month", "day", "hour"], ascending=True)["uploaded_file"].values)

        else:
            
            list_folders = sorted(glob.glob(self.path + "/*/"))
            list_filenames = np.array([])
            
            for i, folder in enumerate(list_folders):
                filenames = glob.glob(os.path.join(folder, "*.csv"))
                self.animal = filenames[1][-30:-25]
                
                list_filenames = np.hstack([list_filenames, filenames])
                
                self.progress_bar.progress((i+1)/len(list_folders))

            self.list_filenames = sorted(list_filenames)


    def checking_light(self):
        # 0 declarando variavies -------------------------------------------------------------------------------------------
        coord = np.array([])
        luz = True
        self.light_on = []

        for k, filename in enumerate(self.list_filenames): ## for geral que irá caminhar por cada filename
            
            # 1 lendo filename ---------------------------------------------------------------------------------------------
            dataSet = pd.read_csv(filename,names = ['a','b','c','d','e','f','g']) ## lendo filename
            dataSet_np = np.array(dataSet) ## transformando em numpy array para ganhar velocidade de processamento
            if st.session_state.checkbox_web_app:
                filename = filename.name
            # --------------------------------------------------------------------------------------------------------------
            
            # 2 separando os dados de tempo e coordenada -------------------------------------------------------------------
            timet = dataSet_np[:,4:] 
            coord = dataSet_np[:,1:3]
            # --------------------------------------------------------------------------------------------------------------
            
            for i in range(len(timet)): ## for que irá caminhar por cada linha da tabela lida
                
                # 3 extraindo os dados de tempo ----------------------------------------------------------------------------
                ano = int(filename[len(filename)-17:len(filename)-13])
                mes = int(self.strtomonth(filename[len(filename)-21:len(filename)-18]))
                dia = int(filename[len(filename)-24:len(filename)-22])
                hora = int(timet[i,0])
                minu = int(timet[i,1])
                seg = int(timet[i,2])
                mics = int(100*(dataSet_np[i,6]%1))
                # ---------------------------------------------------------------------------------------------------------- 
            
                # 4 checando ligar/desligar da luz -------------------------------------------------------------------------
                if coord[i,0] == 160.5 and coord[i,1] == 120.5 and luz == True:
                    print(Back.BLACK + Fore.WHITE + " OFF →", datetime(ano,mes,dia,hora,minu,seg), "", filename, "")
                    luz = False

                elif coord[i,0] != 160.5 and coord[i,1] != 120.5 and luz == False:
                    print(Back.WHITE + Fore.BLACK + " ON  →", datetime(ano,mes,dia,hora,minu,seg), "", filename, "")
                    
                    self.light_on.append(datetime(ano,mes,dia,hora,minu,seg,mics))
                    luz = True
                # ----------------------------------------------------------------------------------------------------------
       
            self.progress_bar.progress((k+1)/len(self.list_filenames))
        
        


    def get_heatmap_df(self):
        
        # 0 declarando variavies -------------------------------------------------------------------------------------------
        quinze_horas = datetime(2019,8,14,21,0,0) - datetime(2019,8,14,6,0,0,0)

        td3h = timedelta(minutes=0, hours=3)
        td5h = timedelta(minutes=0, hours=5)
        td7h30m = timedelta(minutes=30, hours=7)

        list3h = []
        list5h = []
        list7h30m = []
        list_day = []

        count_3h = -1
        count_5h = -1
        count_7h30m = -1
        count_day = -1
        dict_3h = {}
        dict_5h = {}
        dict_7h30m = {}
        dict_day = {}

        format_data = "%d/%m/%y %H:%M:%S"

        first_day = True
        last_day = False
        begin = False
        on = 0

        dia_check = 0 
        mes_check = 0

        index_first_bool = True
        index_first = 0
        index_last = 0
        
        count_filter = 0
        list_filter = []

        for k, filename in enumerate(tq.tqdm(self.list_filenames)): ## for geral que irá caminhar por cada filename
            
            # 1 lendo filename ---------------------------------------------------------------------------------------------
            dataSet = pd.read_csv(filename,names = ['update_rate','coord_x','coord_y','x','time_h','time_m','time_s']) ## lendo filename
            # filtering [0,0] coords
            dataSet = dataSet.loc[~(dataSet[['coord_x','coord_y']]==0).all(axis=1)]
            dataSet_np = np.array(dataSet) ## transformando em numpy array para ganhar velocidade de processamento
            if st.session_state.checkbox_web_app:
                filename = filename.name
            # --------------------------------------------------------------------------------------------------------------
            
            # 2 separando os dados de tempo e coordenada -------------------------------------------------------------------
            timet = dataSet_np[:,4:] 
            # --------------------------------------------------------------------------------------------------------------
            
            for i in range(len(timet)): ## for que irá caminhar por cada linha da tabela lida
                
                # 3 extraindo os dados de tempo ----------------------------------------------------------------------------
                ano = int(filename[len(filename)-17:len(filename)-13])
                mes = int(self.strtomonth(filename[len(filename)-21:len(filename)-18]))
                dia = int(filename[len(filename)-24:len(filename)-22])
                hora = int(timet[i,0])
                minu = int(timet[i,1])
                seg = int(timet[i,2])
                mics = int(100*(dataSet_np[i,6]%1))
                # ---------------------------------------------------------------------------------------------------------- 
                
                # 5 resolvendo problemas ====================================================================================
                # PROBLEMA : quando temos arquivos q começam em um dia e terminam no outro as primeiras linhas receberão er-
                # roneamente os dados de dia e mês do dia seguinte; 
                # OBS.: os dados de ano, mes e dia são retirados do nome do arquivo que são nomeados com a data do final do
                # intervalo de registro (17 minutos).

                if dia_check != dia:
                    if hora == 23:
                        dia = dia_check
                    else:
                        dia_check = dia

                if mes_check != mes:
                    if hora == 23:
                        mes = mes_check
                    else:
                        mes_check = mes
                # ==========================================================================================================
                time = datetime(ano,mes,dia,hora,minu,seg,mics)
                
                # 4 checando ligar/desligar da luz -------------------------------------------------------------------------
                if (time >= self.light_on[on]) and (not last_day):
                    
                    if index_first_bool:
                        index_first = i
                        index_first_bool = False

                    if begin == False:
                        index_first = i
                        
                        print("light on", time)
                        
                        count_3h += 1
                        count_5h += 1
                        count_7h30m += 1
                        count_day += 1

                        target_time_3h = datetime(ano,mes,dia,hora,minu,seg,mics)
                        target_time_5h = datetime(ano,mes,dia,hora,minu,seg,mics)
                        target_time_7h30m = datetime(ano,mes,dia,hora,minu,seg,mics)
                        target_time_day = datetime(ano,mes,dia,hora,minu,seg,mics)
                        
                        dict_3h[count_3h] = target_time_3h.strftime(format_data)
                        dict_5h[count_5h] = target_time_5h.strftime(format_data)
                        dict_7h30m[count_7h30m] = target_time_7h30m.strftime(format_data)
                        dict_day[count_day] = target_time_day.strftime(format_data)

                        begin = True
                        first_day = False

                    else:
                        if time - target_time_3h >= td3h:
                            target_time_3h = datetime(ano,mes,dia,hora,minu,seg,mics)
                            
                            count_3h += 1
                            dict_3h[count_3h] = target_time_3h.strftime(format_data)
                        if time - target_time_5h >= td5h:
                            target_time_5h = datetime(ano,mes,dia,hora,minu,seg,mics)
                            
                            count_5h += 1
                            dict_5h[count_5h] = target_time_5h.strftime(format_data)
                        if time - target_time_7h30m >= td7h30m:
                            target_time_7h30m = datetime(ano,mes,dia,hora,minu,seg,mics)
                            
                            count_7h30m += 1
                            dict_7h30m[count_7h30m] = target_time_7h30m.strftime(format_data)

                    list3h.append(count_3h)
                    list5h.append(count_5h)
                    list7h30m.append(count_7h30m)
                    list_day.append(count_day)
                    
                    if time - self.light_on[on] >= quinze_horas:
                        begin = False
                        
                        index_last = i
                        
                        if on < len(self.light_on)-1:
                            on += 1
                        else:
                            last_day = True
                    
                    index_last = i+1

                # 4 filtro -------------------------------------------------------------------------
                    if not self.filter_file.empty:
                        if self.filter_file["mask"][count_filter]:
                            list_filter.append(False)
                        else:
                            list_filter.append(True)
                count_filter += 1

            if not last_day:
                self.dataSet_all = pd.concat([self.dataSet_all, dataSet.iloc[index_first:index_last,:][["coord_x", "coord_y"]]])
            
            index_first_bool = True
            index_first = 0
            index_last = 0

            self.progress_bar.progress((k+1)/len(self.list_filenames))

        groups_dict = {"day":np.array(list_day).astype(int), "3h":np.array(list3h).astype(int), "5h":np.array(list5h).astype(int), "7h30m":np.array(list7h30m).astype(int)}
        if not self.filter_file.empty:
            groups_dict["filter"] = list_filter
        print(len(list_filter), len(list_day))
        for group in tq.tqdm(groups_dict):
            self.dataSet_all[group] = groups_dict[group]

        self.label_dict = {"3h":dict_3h, "5h":dict_5h, "7h30m":dict_7h30m, "day":dict_day}

def send_email(sender, password, receiver, smtp_server, smtp_port, email_message, subject, attachment=None):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.header import Header
    from email.mime.application import MIMEApplication

    message = MIMEMultipart()
    message['To'] = Header(receiver)
    message['From']  = Header(sender)
    message['Subject'] = Header(subject)
    message.attach(MIMEText(email_message,'plain', 'utf-8'))
    if attachment:
        att = MIMEApplication(attachment.read(), _subtype="txt")
        att.add_header('Content-Disposition', 'attachment', filename=attachment.name)
        message.attach(att)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.ehlo()
    server.login(sender, password)
    text = message.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()