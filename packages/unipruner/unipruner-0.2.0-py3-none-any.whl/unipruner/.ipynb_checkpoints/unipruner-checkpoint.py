import os
import logging
import warnings
from pathlib import Path

import pandas as pnd
import gempipe
import cobra



def check_inputs(logger, universe, eggnog):
    
    
    # check if files exist
    if os.path.isfile(universe) == False: 
        logger.error(f"Provided --universe doesn't exist: {universe}.")
        return 1
    if os.path.isfile(eggnog) == False: 
        logger.error(f"Provided --eggnog doesn't exist: {eggnog}.")
        return 1
    
    
    # check the universe model format
    if universe.endswith('.xml'):
        universe = cobra.io.read_sbml_model(universe)
    else: 
        logger.error(f"Provided --universe must be in cobrapy-compatible SBML format (.xml extension).")
        return 1
    
    
    # log main universe metrics:
    G = len([g.id for g in universe.genes])
    R = len([r.id for r in universe.reactions])
    M = len([m.id for m in universe.metabolites])
    uM = len(set([m.id.rsplit('_', 1)[0] for m in universe.metabolites]))
    gr = len([gr.id for gr in universe.groups])
    bP = len([m.id for m in universe.reactions.get_by_id('Biomass').reactants])
    logger.info(f"Provided universe: [G: {G}, R: {R}, M: {M}, uM: {uM}, gr: {gr}, bP: {bP}, Biomass: {round(universe.slim_optimize(), 3)}]")
        
        
    # load eggnog annotations
    eggnog = pnd.read_csv(eggnog, sep='\t', comment='#', header=None)
    eggnog.columns = 'query	seed_ortholog	evalue	score	eggNOG_OGs	max_annot_lvl	COG_category	Description	Preferred_name	GOs	EC	KEGG_ko	KEGG_Pathway	KEGG_Module	KEGG_Reaction	KEGG_rclass	BRITE	KEGG_TC	CAZy	BiGG_Reaction	PFAMs'.split('\t')
    eggnog = eggnog.set_index('query', drop=True, verify_integrity=True)
    
    return [universe, eggnog]



def parse_eggnog(eggnog):
    
    
    # PART 1. get KO codes available
    gid_to_kos = {}
    ko_to_gids = {}
    for gid, kos in eggnog['KEGG_ko'].items():
        if kos == '-': 
            continue
            
        if gid not in gid_to_kos.keys(): 
            gid_to_kos[gid] = set()
            
        kos = kos.split(',')
        kos = [i.replace('ko:', '') for i in kos]
        for ko in kos: 
            if ko not in ko_to_gids.keys(): 
                ko_to_gids[ko] = set()
                
            # populate dictionaries
            ko_to_gids[ko].add(gid)
            gid_to_kos[gid].add(ko)

    
    return ko_to_gids, gid_to_kos



def get_modeled_kos(model):
    
    
    # get modeled KO ids:
    modeled_gid_to_ko = {}
    modeled_ko_to_gid = {}
    
    for g in model.genes:
        if g.id in ['orphan', 'spontaneous']: 
            continue
        corresponding_ko = g.annotation['ko']
        
        modeled_gid_to_ko[g.id] = corresponding_ko
        modeled_ko_to_gid[corresponding_ko] = g.id
        
    modeled_kos = list(modeled_gid_to_ko.values())
        
    return modeled_kos, modeled_gid_to_ko, modeled_ko_to_gid



def subtract_kos(logger, model, eggonog_ko_to_gids):
    
    
    modeled_kos, _, modeled_ko_to_gid = get_modeled_kos(model)
        
        
    to_remove = []  # genes to delete
    for ko in modeled_kos: 
        if ko not in eggonog_ko_to_gids.keys():
            gid_to_remove = modeled_ko_to_gid[ko]
            to_remove.append(model.genes.get_by_id(gid_to_remove))
    
    
    # delete marked genes!
    # trick to avoid the WARNING "cobra/core/group.py:147: UserWarning: need to pass in a list" 
    # triggered when trying to remove reactions that are included in groups. 
    with warnings.catch_warnings():  # temporarily suppress warnings for this block
        warnings.simplefilter("ignore")  # ignore all warnings
        cobra_logger = logging.getLogger("cobra.util.solver")
        old_level = cobra_logger.level
        cobra_logger.setLevel(logging.ERROR)   

        cobra.manipulation.delete.remove_genes(model, to_remove, remove_reactions=True)

        # restore original behaviour: 
        cobra_logger.setLevel(old_level)   
        
   
    logger.info(f"Found {len(model.genes)} modeled orthologs.")
    return 0



def translate_remaining_kos(logger, model, eggonog_ko_to_gids):
    
    
    _, modeled_gid_to_ko, _ = get_modeled_kos(model) 
    
    
    # iterate reactions:
    for r in model.reactions:

        gpr = r.gene_reaction_rule

        # force each gid to be surrounded by spaces: 
        gpr = ' ' + gpr.replace('(', ' ( ').replace(')', ' ) ') + ' '
        
        for gid in modeled_gid_to_ko.keys():
            if f' {gid} ' in gpr:
                
                new_gids = eggonog_ko_to_gids[modeled_gid_to_ko[gid]]
                gpr = gpr.replace(f' {gid} ', f' ({" or ".join(new_gids)}) ')       
            

        # remove spaces between parenthesis
        gpr = gpr.replace(' ( ', '(').replace(' ) ', ')')
        # remove spaces at the extremes: 
        gpr = gpr[1: -1]


        # New genes are introduced. Parethesis at the extremes are removed if not necessary. 
        r.gene_reaction_rule = gpr
        r.update_genes_from_gpr()
            
            
    # remaining old 'Cluster_'s need to removed.
    # remove if (1) hte ID starts with clusters AND (2) they are no more associated with any reaction
    to_remove = []
    for g in model.genes:
        
        if g.id in ['orphan', 'spontaneous']:
            continue
            
        if g.id in modeled_gid_to_ko.keys() and len(g.reactions)==0:
            to_remove.append(g)
            
    # warning suppression not needed here, as no reaction is actually removed.
    cobra.manipulation.delete.remove_genes(model, to_remove, remove_reactions=True)
    
        
    logger.info(f"Translated orthologs to {len(model.genes)} genes.")
    return 0
        
    
    
    
def check_biosynthesis(logger, model, universe, growth, biosynth, reference):
    
    
    if growth: 
        
        # check production of biomass precursors: 
        logger.info("Checking biosynthesis of every biomass component...")
        
        print()
        mids = gempipe.check_reactants(model, 'Biomass')
        if mids == []: 
            print("No blocked biomass component detected!")
        print()

        
        
    if biosynth != '-':
        
        # check biosynthesis of every modeled metabolite:
        logger.info("Checking biosynthesis of every metabolite...")
        df_rows = []
        for m in model.metabolites:
            if m.id.endswith('_c'):
                binary, obj_value, status = gempipe.can_synth(model, m.id)
                df_rows.append({'mid': m.id, 'binary': binary, 'obj_value': obj_value, 'status': status})
        df_rows = pnd.DataFrame.from_records(df_rows)
        df_rows = df_rows.set_index('mid', drop=True, verify_integrity=True)
        
        # save table as excel: 
        df_rows.to_excel('biosynth.xlsx')
        logger.info(f"'{os.getcwd()}/biosynth.xlsx' created!")
        
        
        
        # focus on a particular metabolite:
        modeld_mids = [m.id for m in model.metabolites]
        if not (biosynth in modeld_mids and biosynth.endswith('_c')):
            logger.error(f"Cytosolic metabolite defined with --biosynth is not included: '{biosynth}'.")
            return 1
        
        nsol = 5   # number of solutions
        logger.info(f"Computing {nsol} gapfilling solutions for cytosolic metabolite {biosynth}...")

        
        # if provided, use the reference model as repository of reactions
        if reference != '-':   
            if reference.endswith('.xml'):
                refmodel = cobra.io.read_sbml_model(reference)
            elif reference.endswith('.json'):
                refmodel = cobra.io.load_json_model(reference)
            else:
                logger.error(f"Likely unsupported format found in --reference. Please use '.xml' or '.json'.")
                return 1
            repository = refmodel
        else:
            repository = universe
            

        # remove genes to avoid the "ValueError: id purP is already present in list"
        repository_nogenes = repository.copy()
        cobra.manipulation.delete.remove_genes(repository_nogenes, [g.id for g in repository_nogenes.genes], remove_reactions=False)
        
        
        # model and universe are already set up with the same growth medium:
        print()
        # perform gap-filling, solutions are shown using print()
        _ = gempipe.perform_gapfilling(model, repository_nogenes, biosynth, nsol=nsol)
        print()
             
    
    return 0

    

def unipruner(args, logger): 
    
    
    
    # check input files:
    response = check_inputs(logger, args.universe, args.eggnog)
    if type(response)==int:
        return 1
    universe = response[0]
    eggnog = response[1]
    
    
    # get important dictionaries: 'eggnog_ko_to_gids' and 'eggonog_gid_to_kos'
    eggnog_ko_to_gids, eggonog_gid_to_kos = parse_eggnog(eggnog)
    
    # make a copy
    model = universe.copy()
    model.id = Path(args.eggnog).stem 
    
            
    # substract missing KOs
    subtract_kos(logger, model, eggnog_ko_to_gids)
    translate_remaining_kos(logger, model, eggnog_ko_to_gids)
    
    
    # output the model:
    cobra.io.save_json_model(model, f'{model.id}.json')
    cobra.io.write_sbml_model(model, f'{model.id}.xml')   # groups are saved only to SBML 
    G = len([g.id for g in model.genes])
    R = len([r.id for r in model.reactions])
    M = len([m.id for m in model.metabolites])
    uM = len(set([m.id.rsplit('_', 1)[0] for m in model.metabolites]))
    gr = len([gr.id for gr in model.groups])
    bP = len([m.id for m in model.reactions.get_by_id('Biomass').reactants])
    logger.info(f"'{os.getcwd()}/{model.id}.json' created!")
    logger.info(f"'{os.getcwd()}/{model.id}.xml' created!")
    logger.info(f"Resulting model: [G: {G}, R: {R}, M: {M}, uM: {uM}, gr: {gr}, bP: {bP}, Biomass: {round(model.slim_optimize(), 3)}]")
    
    
    response = check_biosynthesis(logger, model, universe, args.growth, args.biosynth, args.reference)
    if response==1: return 1

    
    return 0