import sunspec2.file.client as client

class Test:
    
    def __init__(self, json_file):
        self.inv = client.FileClientDevice(json_file)
        self.inv.scan()
        models = self.get_models()
        self.print_modbus_map(models,True)

    def close(self):
        if self.inv is not None:
            self.inv.close()
            self.inv = None
    

    def get_models(self):
        """ Get SunSpec Models
            :return: list of models
        """
        if self.inv is None:
            raise der1547.DER1547Error('DER not initialized')
        
        model_dict = self.inv.models
        models = []
        for k in model_dict.keys():
            if not isinstance(k, int) and k is not None:
                models.append(k)
        return models



    def print_modbus_map(self, models=None, w_labels=None):
        """
        Prints the modbus map of the DER device
        :param models: model or models to read, if None read all
        :param w_labels: if True, print the modbus points with labels included
        :return: None
        """
        model_list = []
        if models is None:
            model_list = self.get_models()
        elif isinstance(models, str):
            model_list = [models]
        elif isinstance(models, list):
            model_list = models
            #else:
            # der1547.DER1547Error('Incorrect model format for printing modbus map.')

        if not w_labels:
            for m in model_list:
                mod = eval('self.inv.%s[0]' % m)
                self.ts.log('%s' % mod)
        else:
            print(model_list)
            for m in model_list:
                #self.ts.log('-'*50)
                #self.ts.log('Model: %s' % m)
                print('Model: %s' + str(m))
                #self.ts.log('')
                for pt in eval('self.inv.%s[0].points.keys()' % m):
                    # self.ts.log_debug('pt: %s' % pt)
                    if pt != 'Pad':
                        label = eval('self.inv.%s[0].points[pt].pdef["label"]' % m)
                        val = eval('self.inv.%s[0].points[pt].cvalue' % m)

                        if val is not None and eval('self.inv.%s[0].points[pt].pdef.get("symbols")' % m) is not None:
                            symbol = eval('self.inv.%s[0].points[pt].pdef.get("symbols")' % m)
                            # self.ts.log('Symbols: %s' % symbol)
                            symb = None
                            if symbol is not None:
                                if isinstance(symbol, list):
                                    for s in symbol:
                                        # self.ts.log('s: %s' % s)
                                        if val == s.get('value'):
                                            symb = s.get("label")
                                else:
                                    if symbol.get(val) is not None:
                                        symb = eval('self.inv.%s[0].points[pt].pdef["symbols"][val]["label"]' % m)
                            self.ts.log('%s [%s]: %s [%s]' % (label, pt, val, symb))
                        else:
                            self.ts.log('%s [%s]: %s' % (label, pt, val))

                # Cycle through groups
                self.print_group(group_obj=eval('self.inv.%s[0]' % m))

test = Test('sunspec_device_1547.json')

