import { Component, Input } from "@angular/core";

@Component({
  selector: "zh-details-fonctions",
  templateUrl: "./fonctions.component.html",
  styleUrls: ["./fonctions.component.scss"],
})
export class FonctionsComponent {
  @Input() data;

  public hydroFctTableCol = [
    { name: "type", label: "Fonctions hydrologiques" },
    { name: "justification", label: "Justifications" },
    { name: "qualification", label: "Qualifications" },
    { name: "connaissance", label: "Connaissance" },
  ];
  public bioFctTableCol = [
    { name: "type", label: "Fonctions biologiques" },
    { name: "justification", label: "Justifications" },
    { name: "qualification", label: "Qualifications" },
    { name: "connaissance", label: "Connaissance" },
  ];
  public intertesTableCol = [
    { name: "type", label: "Intérêts patrimoniaux" },
    { name: "justification", label: "Justifications" },
    { name: "qualification", label: "Qualifications" },
    { name: "connaissance", label: "Connaissance" },
  ];

  public corineTableCol = [
    { name: "biotope", label: "Corine Biotope" },
    { name: "etat", label: "État de conservation" },
    { name: "cahier", label: "Cahier Habitats" },
    { name: "recouvrement", label: "Recouvrement de la ZH (%)" },
  ];

  public socioEcoTableCol = [
    { name: "type", label: "Valeurs socio-économiques" },
    { name: "justification", label: "Justifications" },
    { name: "qualification", label: "Qualifications" },
    { name: "connaissance", label: "Connaissance" },
  ];
}
