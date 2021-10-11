import { RenseignementsGenerauxModel } from "./renseignements.model";
import { DelimitationModel } from "./delimitation.model";
import { DescriptionModel } from "./description.model";
import { FonctionnementModel } from "./fonctionnement.model";
import { FonctionsModel } from "./fonctions.model";
import { StatutsModel } from "./status.model";
import { EvaluationModel } from "./evaluations.model";

export interface DetailsModel {
  renseignements: RenseignementsGenerauxModel;
  delimitation: DelimitationModel;
  description: DescriptionModel;
  fonctionnement: FonctionnementModel;
  fonctions: FonctionsModel;
  statuts: StatutsModel;
  evaluation: EvaluationModel;
}
