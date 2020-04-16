

models = dict()

models['Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Batch'] = \
    {
    'Yox_XG': {
        'description' : 'Yield for the oxidative pathway of glucose to biomass',
        'slider_min_value' : 0.2,
        'slider_max_value' : 1.2,
        'slider_step_value' : 0.1,
        'value':0.8
    },
        'Yred_XG': {
            'description' : 'Yield of the reductive pathway of glucose to biomass',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.05
    },
    'Yox_XE':
        {
            'description' : 'Yield of the pathway of ethanol to biomass',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.72
    },
     'Y_OG':
         {
            'description' : 'Yield of the need of oxygen to glucose',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 1.067
    },
     'Y_EG': {
            'description' : 'Yield of the need of ethanol to glucose',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.5
    },

     'q_o':
         {
            'description' : 'Maximal specific oxygen uptake rate',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.37
    },

    'q_g':
        {
            'description':  'Maximal specific glucose uptake rate',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 3.5
        },

    'q_e':  {
            'description' :  'Maximal specific ethanol uptake rate',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.32
    },
     't_lag':  {
            'description' :'Lag time',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 4.66
    },

     'Kg':  {
            'description' : 'Affinity constant for glucose uptake',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.17
    },

    'Ke':  {
            'description' :'Affinity constant for ethanol uptake',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.56
    },

    'Ko':  {
            'description' : 'Affinity constant for oxygen uptake',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.0001
    },

     'Ki':  {
            'description' :'Inhibition parameter: free glucose inhibits ethanol uptake',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.31
    },

     'O_sat':  {
            'description' : 'Concentration of saturated oxygen',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.00755
    },

     'kla':  {
            'description' : 'Mass transfer coefficient for oxygen',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 1004
    },

    'G0':  {
            'description' : 'Initial concentration of glucose',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 18
    },

    'O0':  {
            'description' : 'Initial concentration of oxygen',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value':0.0755
    },

    'E0':  {
            'description' : 'Initial concentration of ethanol',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.8
    },

    'X0':  {
            'description' : 'Initial concentration of biomass',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.1
    }

}
models['Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Fedbatch'] = \
    {
        'Yox_XG': {
            'description': 'Yield for the oxidative pathway of glucose to biomass',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.8
        },
        'Yred_XG': {
            'description': 'Yield of the reductive pathway of glucose to biomass',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.05
        },
        'Yox_XE':
            {
                'description': 'Yield of the pathway of ethanol to biomass',
                'slider_min_value': 0.2,
                'slider_max_value': 1.2,
                'slider_step_value': 0.1,
                'value': 0.72
            },
        'Y_OG':
            {
                'description': 'Yield of the need of oxygen to glucose',
                'slider_min_value': 0.2,
                'slider_max_value': 1.2,
                'slider_step_value': 0.1,
                'value': 1.067
            },
        'Y_EG': {
            'description': 'Yield of the need of ethanol to glucose',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.5
        },

        'q_o':
            {
                'description': 'Maximal specific oxygen uptake rate',
                'slider_min_value': 0.2,
                'slider_max_value': 1.2,
                'slider_step_value': 0.1,
                'value': 0.37
            },

        'q_g':
            {
                'description': 'Maximal specific glucose uptake rate',
                'slider_min_value': 0.2,
                'slider_max_value': 1.2,
                'slider_step_value': 0.1,
                'value': 3.5
            },

        'q_e': {
            'description': 'Maximal specific ethanol uptake rate',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.32
        },
        't_lag': {
            'description': 'Lag time',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 4.66
        },

        'Kg': {
            'description': 'Affinity constant for glucose uptake',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.17
        },

        'Ke': {
            'description': 'Affinity constant for ethanol uptake',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.56
        },

        'Ko': {
            'description': 'Affinity constant for oxygen uptake',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.0001
        },

        'Ki': {
            'description': 'Inhibition parameter: free glucose inhibits ethanol uptake',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.31
        },

        'O_sat': {
            'description': 'Concentration of saturated oxygen',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.00755
        },

        'kla': {
            'description': 'Mass transfer coefficient for oxygen',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 1004
        },

        'G0': {
            'description': 'Initial concentration of glucose',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 18
        },

        'O0': {
            'description': 'Initial concentration of oxygen',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value':0.0755
        },

        'E0': {
            'description': 'Initial concentration of ethanol',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.8
        },

        'X0': {
            'description': 'Initial concentration of biomass',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.1
        }

    }

models['Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Cstr'] = \
    {
        'Yox_XG': {
            'description': 'Yield for the oxidative pathway of glucose to biomass',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.8
        },
        'Yred_XG': {
            'description': 'Yield of the reductive pathway of glucose to biomass',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.05
        },
        'Yox_XE':
            {
                'description': 'Yield of the pathway of ethanol to biomass',
                'slider_min_value': 0.2,
                'slider_max_value': 1.2,
                'slider_step_value': 0.1,
                'value': 0.72
            },
        'Y_OG':
            {
                'description': 'Yield of the need of oxygen to glucose',
                'slider_min_value': 0.2,
                'slider_max_value': 1.2,
                'slider_step_value': 0.1,
                'value': 1.067
            },
        'Y_EG': {
            'description': 'Yield of the need of ethanol to glucose',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.5
        },

        'q_o':
            {
                'description': 'Maximal specific oxygen uptake rate',
                'slider_min_value': 0.2,
                'slider_max_value': 1.2,
                'slider_step_value': 0.1,
                'value': 0.37
            },

        'q_g':
            {
                'description': 'Maximal specific glucose uptake rate',
                'slider_min_value': 0.2,
                'slider_max_value': 1.2,
                'slider_step_value': 0.1,
                'value': 3.5
            },

        'q_e': {
            'description': 'Maximal specific ethanol uptake rate',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.32
        },
        't_lag': {
            'description': 'Lag time',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 4.66
        },

        'Kg': {
            'description': 'Affinity constant for glucose uptake',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.17
        },

        'Ke': {
            'description': 'Affinity constant for ethanol uptake',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.56
        },

        'Ko': {
            'description': 'Affinity constant for oxygen uptake',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.0001
        },

        'Ki': {
            'description': 'Inhibition parameter: free glucose inhibits ethanol uptake',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.31
        },

        'O_sat': {
            'description': 'Concentration of saturated oxygen',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.00755
        },

        'kla': {
            'description': 'Mass transfer coefficient for oxygen',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 1004
        },

        'G0': {
            'description': 'Initial concentration of glucose',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 18
        },

        'O0': {
            'description': 'Initial concentration of oxygen',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value':0.0755
        },

        'E0': {
            'description': 'Initial concentration of ethanol',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.8
        },

        'X0': {
            'description': 'Initial concentration of biomass',
            'slider_min_value': 0.2,
            'slider_max_value': 1.2,
            'slider_step_value': 0.1,
            'value': 0.1
        }

    }