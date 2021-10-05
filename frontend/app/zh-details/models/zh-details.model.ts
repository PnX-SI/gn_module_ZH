import { RenseignementsGenerauxModel } from "./renseignements.model";
import { DelimitationModel } from "./delimitation.model";
import { DescriptionModel } from "./description.model";
import { FonctionnementModel } from "./fonctionnement.model";
import { FonctionsModel } from "./fonctions.model";
import { StatutsModel } from "./status.model";
import { EvaluationModel } from "./evaluations.model";

export interface DetailsModel {
  "1- Renseignements généraux": RenseignementsGenerauxModel;
  "2- Délimitation de la zone humide et de l'espace de fonctionnalité": DelimitationModel;
  "3- Description du bassin versant et de la zone humide": DescriptionModel;
  "4- Fonctionnement de la zone humide": FonctionnementModel;
  "5- Fonctions écologiques, valeurs socio-écologiques, intérêt patrimonial": FonctionsModel;
  "6- Statuts et gestion de la zone humide": StatutsModel;
  "7- Evaluation générale du site": EvaluationModel;
}
