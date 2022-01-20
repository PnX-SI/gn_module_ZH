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
    { name: "qualification", label: "Qualifications" },
    { name: "connaissance", label: "Connaissance" },
    { name: "justification", label: "Justifications" },
  ];
  public bioFctTableCol = [
    { name: "type", label: "Fonctions biologiques" },
    { name: "qualification", label: "Qualifications" },
    { name: "connaissance", label: "Connaissance" },
    { name: "justification", label: "Justifications" },
  ];
  public intertesTableCol = [
    { name: "type", label: "Intérêts patrimoniaux" },
    { name: "qualification", label: "Qualifications" },
    { name: "connaissance", label: "Connaissance" },
    { name: "justification", label: "Justifications" },
  ];

  public corineTableCol = [
    { name: "biotope", label: "Corine Biotope" },
    { name: "cahier", label: "Cahier Habitats" },
    { name: "etat", label: "État de conservation" },
    { name: "recouvrement", label: "Recouvrement de la ZH (%)" },
  ];

  public socioEcoTableCol = [
    { name: "type", label: "Valeurs socio-économiques" },
    { name: "qualification", label: "Qualifications" },
    { name: "connaissance", label: "Connaissance" },
    { name: "justification", label: "Justifications" },
  ];
}
