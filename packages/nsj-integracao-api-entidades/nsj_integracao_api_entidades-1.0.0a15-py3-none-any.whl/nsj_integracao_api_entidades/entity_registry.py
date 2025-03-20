import os
import importlib
import inspect

class EntityRegistry:

    _entities = {}

    _dtos = {}

    _entities_ = [
        'nsj_integracao_api_entidades.entity.financas_agencias',
        'nsj_integracao_api_entidades.entity.financas_bancos',
        'nsj_integracao_api_entidades.entity.ns_configuracoes',
        'nsj_integracao_api_entidades.entity.ns_empresas',
        'nsj_integracao_api_entidades.entity.ns_estabelecimentos',
        'nsj_integracao_api_entidades.entity.ns_feriados',
        'nsj_integracao_api_entidades.entity.ns_gruposempresariais',
        'nsj_integracao_api_entidades.entity.ns_obras',
        'nsj_integracao_api_entidades.entity.persona_adiantamentosavulsos',
        'nsj_integracao_api_entidades.entity.persona_admissoespreliminares',
        'nsj_integracao_api_entidades.entity.persona_afastamentostrabalhadores',
        'nsj_integracao_api_entidades.entity.persona_ambientes',
        'nsj_integracao_api_entidades.entity.persona_avisosferiastrabalhadores',
        'nsj_integracao_api_entidades.entity.persona_avisospreviostrabalhadores',
        'nsj_integracao_api_entidades.entity.persona_beneficios',
        'nsj_integracao_api_entidades.entity.persona_beneficiostrabalhadores',
        'nsj_integracao_api_entidades.entity.persona_calculostrabalhadores',
        'nsj_integracao_api_entidades.entity.persona_cargos',
        'nsj_integracao_api_entidades.entity.persona_compromissostrabalhadores',
        'nsj_integracao_api_entidades.entity.persona_concessionariasvts',
        'nsj_integracao_api_entidades.entity.persona_condicoesambientestrabalho',
        'nsj_integracao_api_entidades.entity.persona_configuracoesordemcalculomovimentosponto',
        'nsj_integracao_api_entidades.entity.persona_configuracoesordemcalculomovimentos',
        'nsj_integracao_api_entidades.entity.persona_convocacoestrabalhadores',
        'nsj_integracao_api_entidades.entity.persona_departamentos',
        'nsj_integracao_api_entidades.entity.persona_dependentestrabalhadores',
        'nsj_integracao_api_entidades.entity.persona_dispensavalestransportestrabalhadores',
        'nsj_integracao_api_entidades.entity.persona_documentoscolaboradores',
        'nsj_integracao_api_entidades.entity.persona_emprestimostrabalhadores',
        'nsj_integracao_api_entidades.entity.persona_escalasfolgastrabalhadores',
        'nsj_integracao_api_entidades.entity.persona_eventos',
        'nsj_integracao_api_entidades.entity.persona_faixas',
        'nsj_integracao_api_entidades.entity.persona_faltastrabalhadores',
        'nsj_integracao_api_entidades.entity.persona_funcoes',
        'nsj_integracao_api_entidades.entity.persona_gestorestrabalhadores',
        'nsj_integracao_api_entidades.entity.persona_historicosadiantamentosavulsos',
        'nsj_integracao_api_entidades.entity.persona_historicos',
        'nsj_integracao_api_entidades.entity.persona_horariosalternativostrabalhadores',
        'nsj_integracao_api_entidades.entity.persona_horariosespeciais',
        'nsj_integracao_api_entidades.entity.persona_horarios',
        'nsj_integracao_api_entidades.entity.persona_instituicoes',
        'nsj_integracao_api_entidades.entity.persona_intervalosjornadas',
        'nsj_integracao_api_entidades.entity.persona_itensfaixas',
        'nsj_integracao_api_entidades.entity.persona_jornadas',
        'nsj_integracao_api_entidades.entity.persona_lotacoes',
        'nsj_integracao_api_entidades.entity.persona_medicos',
        'nsj_integracao_api_entidades.entity.persona_membroscipa',
        'nsj_integracao_api_entidades.entity.persona_movimentosponto',
        'nsj_integracao_api_entidades.entity.persona_movimentos',
        'nsj_integracao_api_entidades.entity.persona_mudancastrabalhadores',
        'nsj_integracao_api_entidades.entity.persona_niveiscargos',
        'nsj_integracao_api_entidades.entity.persona_outrosrecebimentostrabalhadores',
        'nsj_integracao_api_entidades.entity.persona_outrosrendimentostrabalhadores',
        'nsj_integracao_api_entidades.entity.persona_pendenciaspagamentos',
        'nsj_integracao_api_entidades.entity.persona_processos',
        'nsj_integracao_api_entidades.entity.persona_processosrubricas',
        'nsj_integracao_api_entidades.entity.persona_processossuspensoes',
        'nsj_integracao_api_entidades.entity.persona_reajustessindicatos',
        'nsj_integracao_api_entidades.entity.persona_reajustestrabalhadores',
        'nsj_integracao_api_entidades.entity.persona_rubricasapontamento',
        'nsj_integracao_api_entidades.entity.persona_rubricasponto',
        'nsj_integracao_api_entidades.entity.persona_sindicatos',
        'nsj_integracao_api_entidades.entity.persona_tarifasconcessionariasvts',
        'nsj_integracao_api_entidades.entity.persona_tarifasconcessionariasvtstrabalhadores',
        'nsj_integracao_api_entidades.entity.persona_tiposanexos',
        'nsj_integracao_api_entidades.entity.persona_tiposdocumentoscolaboradores',
        'nsj_integracao_api_entidades.entity.persona_tiposfuncionarios',
        'nsj_integracao_api_entidades.entity.persona_tiposhistoricos',
        'nsj_integracao_api_entidades.entity.persona_trabalhadores',
        'nsj_integracao_api_entidades.entity.persona_valestransportespersonalizadostrabalhadores',
        'nsj_integracao_api_entidades.entity.ponto_atrasosentradascompensaveistrabalhadores',
        'nsj_integracao_api_entidades.entity.ponto_compensacoeslancamentos',
        'nsj_integracao_api_entidades.entity.ponto_diascompensacoestrabalhadores',
        'nsj_integracao_api_entidades.entity.ponto_pagamentoslancamentos',
        'nsj_integracao_api_entidades.entity.ponto_pendenciascalculostrabalhadores',
        'nsj_integracao_api_entidades.entity.ponto_regras',
        'nsj_integracao_api_entidades.entity.ponto_saidasantecipadascompensaveistrabalhadores'
    ]

    _dtos_ = [
        'nsj_integracao_api_entidades.dto.financas_agencias',
        'nsj_integracao_api_entidades.dto.financas_bancos',
        'nsj_integracao_api_entidades.dto.ns_configuracoes',
        'nsj_integracao_api_entidades.dto.ns_empresas',
        'nsj_integracao_api_entidades.dto.ns_estabelecimentos',
        'nsj_integracao_api_entidades.dto.ns_feriados',
        'nsj_integracao_api_entidades.dto.ns_gruposempresariais',
        'nsj_integracao_api_entidades.dto.ns_obras',
        'nsj_integracao_api_entidades.dto.persona_adiantamentosavulsos',
        'nsj_integracao_api_entidades.dto.persona_admissoespreliminares',
        'nsj_integracao_api_entidades.dto.persona_afastamentostrabalhadores',
        'nsj_integracao_api_entidades.dto.persona_ambientes',
        'nsj_integracao_api_entidades.dto.persona_avisosferiastrabalhadores',
        'nsj_integracao_api_entidades.dto.persona_avisospreviostrabalhadores',
        'nsj_integracao_api_entidades.dto.persona_beneficios',
        'nsj_integracao_api_entidades.dto.persona_beneficiostrabalhadores',
        'nsj_integracao_api_entidades.dto.persona_calculostrabalhadores',
        'nsj_integracao_api_entidades.dto.persona_cargos',
        'nsj_integracao_api_entidades.dto.persona_compromissostrabalhadores',
        'nsj_integracao_api_entidades.dto.persona_concessionariasvts',
        'nsj_integracao_api_entidades.dto.persona_condicoesambientestrabalho',
        'nsj_integracao_api_entidades.dto.persona_configuracoesordemcalculomovimentosponto',
        'nsj_integracao_api_entidades.dto.persona_configuracoesordemcalculomovimentos',
        'nsj_integracao_api_entidades.dto.persona_convocacoestrabalhadores',
        'nsj_integracao_api_entidades.dto.persona_departamentos',
        'nsj_integracao_api_entidades.dto.persona_dependentestrabalhadores',
        'nsj_integracao_api_entidades.dto.persona_dispensavalestransportestrabalhadores',
        'nsj_integracao_api_entidades.dto.persona_documentoscolaboradores',
        'nsj_integracao_api_entidades.dto.persona_emprestimostrabalhadores',
        'nsj_integracao_api_entidades.dto.persona_escalasfolgastrabalhadores',
        'nsj_integracao_api_entidades.dto.persona_eventos',
        'nsj_integracao_api_entidades.dto.persona_faixas',
        'nsj_integracao_api_entidades.dto.persona_faltastrabalhadores',
        'nsj_integracao_api_entidades.dto.persona_funcoes',
        'nsj_integracao_api_entidades.dto.persona_gestorestrabalhadores',
        'nsj_integracao_api_entidades.dto.persona_historicosadiantamentosavulsos',
        'nsj_integracao_api_entidades.dto.persona_historicos',
        'nsj_integracao_api_entidades.dto.persona_horariosalternativostrabalhadores',
        'nsj_integracao_api_entidades.dto.persona_horariosespeciais',
        'nsj_integracao_api_entidades.dto.persona_horarios',
        'nsj_integracao_api_entidades.dto.persona_instituicoes',
        'nsj_integracao_api_entidades.dto.persona_intervalosjornadas',
        'nsj_integracao_api_entidades.dto.persona_itensfaixas',
        'nsj_integracao_api_entidades.dto.persona_jornadas',
        'nsj_integracao_api_entidades.dto.persona_lotacoes',
        'nsj_integracao_api_entidades.dto.persona_medicos',
        'nsj_integracao_api_entidades.dto.persona_membroscipa',
        'nsj_integracao_api_entidades.dto.persona_movimentosponto',
        'nsj_integracao_api_entidades.dto.persona_movimentos',
        'nsj_integracao_api_entidades.dto.persona_mudancastrabalhadores',
        'nsj_integracao_api_entidades.dto.persona_niveiscargos',
        'nsj_integracao_api_entidades.dto.persona_outrosrecebimentostrabalhadores',
        'nsj_integracao_api_entidades.dto.persona_outrosrendimentostrabalhadores',
        'nsj_integracao_api_entidades.dto.persona_pendenciaspagamentos',
        'nsj_integracao_api_entidades.dto.persona_processos',
        'nsj_integracao_api_entidades.dto.persona_processosrubricas',
        'nsj_integracao_api_entidades.dto.persona_processossuspensoes',
        'nsj_integracao_api_entidades.dto.persona_reajustessindicatos',
        'nsj_integracao_api_entidades.dto.persona_reajustestrabalhadores',
        'nsj_integracao_api_entidades.dto.persona_rubricasapontamento',
        'nsj_integracao_api_entidades.dto.persona_rubricasponto',
        'nsj_integracao_api_entidades.dto.persona_sindicatos',
        'nsj_integracao_api_entidades.dto.persona_tarifasconcessionariasvts',
        'nsj_integracao_api_entidades.dto.persona_tarifasconcessionariasvtstrabalhadores',
        'nsj_integracao_api_entidades.dto.persona_tiposanexos',
        'nsj_integracao_api_entidades.dto.persona_tiposdocumentoscolaboradores',
        'nsj_integracao_api_entidades.dto.persona_tiposfuncionarios',
        'nsj_integracao_api_entidades.dto.persona_tiposhistoricos',
        'nsj_integracao_api_entidades.dto.persona_trabalhadores',
        'nsj_integracao_api_entidades.dto.persona_valestransportespersonalizadostrabalhadores',
        'nsj_integracao_api_entidades.dto.ponto_atrasosentradascompensaveistrabalhadores',
        'nsj_integracao_api_entidades.dto.ponto_compensacoeslancamentos',
        'nsj_integracao_api_entidades.dto.ponto_diascompensacoestrabalhadores',
        'nsj_integracao_api_entidades.dto.ponto_pagamentoslancamentos',
        'nsj_integracao_api_entidades.dto.ponto_pendenciascalculostrabalhadores',
        'nsj_integracao_api_entidades.dto.ponto_regras',
        'nsj_integracao_api_entidades.dto.ponto_saidasantecipadascompensaveistrabalhadores'
    ]

    def entity_for(self, entity_name: str):
        if len(self._entities)==0:
            for nome_modulo in self._entities_:
                modulo = importlib.import_module(nome_modulo)
                s = nome_modulo.removeprefix("nsj_integracao_api_entidades.entity.")
                # Substitui o primeiro "_" por "."
                partes = s.split("_", 1)
                _tabela = ".".join(partes) if len(partes) == 2 else s
                for _nome, _classe in inspect.getmembers(modulo, inspect.isclass):
                    if _classe.__module__ == nome_modulo:
                        self._entities[_tabela] = _classe

        _classe = self._entities.get(entity_name)
        if _classe is None:
            raise KeyError(f"Não existe uma Entidade correpondente a tabela {entity_name}")

        return _classe

    def dto_for(self, entity_name: str):
        if len(self._dtos)==0:
            for nome_modulo in self._dtos_:
                modulo = importlib.import_module(nome_modulo)
                s = nome_modulo.removeprefix("nsj_integracao_api_entidades.dto.")
                # Substitui o primeiro "_" por "."
                partes = s.split("_", 1)
                _tabela = ".".join(partes) if len(partes) == 2 else s
                for _nome, _classe in inspect.getmembers(modulo, inspect.isclass):
                    if _classe.__module__ == nome_modulo:
                        self._dtos[_tabela] = _classe

        _classe = self._dtos.get(entity_name)
        if _classe is None:
            raise KeyError(f"Não existe um DTO correpondente a tabela {entity_name}")

        return _classe

    def entity_for_v2(self, entity_name: str):
        if len(self._entities)==0:
            for files in os.listdir(os.path.join(os.path.dirname(__file__), 'entity')):
            #for files in os.listdir(f"{os.getcwd()}/entity/"):
                if files.endswith('') and files!='__init__':
                    nome_modulo = f'nsj_integracao_api_entidades.entity.{files[:-3]}'
                    modulo = importlib.import_module(nome_modulo)
                    for _nome, _classe in inspect.getmembers(modulo, inspect.isclass):
                        if _classe.__module__ == nome_modulo:
                            self._entities[files[:-3].replace('_','.')] = _classe

        _classe = self._entities.get(entity_name)
        if _classe is None:
            raise KeyError(f"Não existe uma Entidade correpondente a tabela {entity_name}")

        return _classe

    def dto_for_v2(self, entity_name: str):
        if len(self._dtos)==0:
            #for files in os.listdir(f"{os.getcwd()}/dto/"):
            for files in os.listdir(os.path.join(os.path.dirname(__file__), 'dto')):
                if files.endswith('') and files!='__init__':
                    nome_modulo = f'nsj_integracao_api_entidades.dto.{files[:-3]}'
                    modulo = importlib.import_module(nome_modulo)
                    for _nome, _classe in inspect.getmembers(modulo, inspect.isclass):
                        if _classe.__module__ == nome_modulo:
                            self._dtos[files[:-3].replace('_','.')] = _classe

        _classe = self._dtos.get(entity_name)
        if _classe is None:
            raise KeyError(f"Não existe um DTO correpondente a tabela {entity_name}")

        return _classe