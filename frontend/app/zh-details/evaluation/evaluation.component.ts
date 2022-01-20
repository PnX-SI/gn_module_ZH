import { Component, Input } from "@angular/core";

import { TableColumn } from "../../commonComponents/table/table-interface";
import { EvaluationModel } from "../models/evaluations.model";

@Component({
  selector: "zh-details-evaluation",
  templateUrl: "./evaluation.component.html",
  styleUrls: ["./evaluation.component.scss"],
})
export class EvaluationComponent {
  @Input() data: EvaluationModel;

  readonly qualifSize: string = "10%";
  readonly knowledgeSize: string = "15%";

  public hydroFunctionsCols: TableColumn[] = [
    {
      name: "type",
      label: "Principales fonctions hydrologiques / biogéochimiques",
    },
    { name: "qualification", label: "Qualifications", size: this.qualifSize},
    { name: "connaissance", label: "Connaissance", size: this.knowledgeSize },
  ];

  public bioFunctionsCols: TableColumn[] = [
    { name: "type", label: "Principales fonctions biologiques / écologiques" },
    { name: "qualification", label: "Qualifications", size: this.qualifSize },
    { name: "connaissance", label: "Connaissance", size: this.knowledgeSize },
  ];

  public patrimonialInterestsCols: TableColumn[] = [
    { name: "type", label: "Intérêts patrimoniaux" },
    { name: "qualification", label: "Qualifications", size: this.qualifSize },
    { name: "connaissance", label: "Connaissance", size: this.knowledgeSize },
  ];

  public nbFauneFloreCols: TableColumn[] = [
    {
      name: "faunistique",
      label: "Nombre d'espèces faunistiques patrimoniales",
    },
    {
      name: "floristique",
      label: "Nombre d'espèces floristiques patrimoniales",
    },
  ];

  public nbHabCols: TableColumn[] = [
    {
      name: "nb_hab",
      label: "Nombre d'habitats naturels humides patrimoniaux",
    },
    { name: "total_hab_cover", label: "Recouvrement total sur la ZH (%)" },
  ];

  public valCols: TableColumn[] = [
    { name: "type", label: "Principales values socio-économiques" },
    { name: "qualification", label: "Qualifications", size: this.qualifSize },
    { name: "connaissance", label: "Connaissance", size: this.knowledgeSize },
  ];

  public propositionsCol: TableColumn[] = [
    { name: "proposition", label: "Propositions d'actions" },
    { name: "niveau", label: "Niveau de priorité" },
    { name: "remarque", label: "Remarques" },
  ];

  public menacesCols: TableColumn[] = [
    {
      name: "menaces",
      label: "Évaluation globale des menaces potentielles ou avérées",
    },
    {
      name: "hydrologique",
      label: "Fonctionnalité hydrologique / biogéochimique",
    },
    { name: "biologique", label: "Fonctionnalité biologique / écologique" },
  ];

  getFauneFloreData() {
    return [
      {
        faunistique: this.data.interet.faunistique,
        floristique: this.data.interet.floristique,
      },
    ];
  }

  getHabitatData() {
    return [
      {
        nb_hab: this.data.interet.nb_hab,
        total_hab_cover: this.data.interet.total_hab_cover,
      },
    ];
  }

  getBilanData() {
    return [
      {
        menaces: this.data.bilan.menaces,
        hydrologique: this.data.bilan.hydrologique,
        biologique: this.data.bilan.biologique,
      },
    ];
  }
}
