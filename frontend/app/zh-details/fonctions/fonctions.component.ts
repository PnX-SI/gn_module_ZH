import { Component, Input } from "@angular/core";

@Component({
  selector: "zh-details-fonctions",
  templateUrl: "./fonctions.component.html",
  styleUrls: ["./fonctions.component.scss"],
})
export class FonctionsComponent {
  @Input() data;

  readonly functionSize: string = "30%";
  readonly qualifSize: string = "10%";
  readonly knowledgeSize: string = "10%";

  public hydroFctTableCol = [
    { name: "type", label: "Fonctions hydrologiques", size: this.functionSize },
    { name: "qualification", label: "Qualifications", size: this.qualifSize },
    { name: "connaissance", label: "Connaissance", size: this.knowledgeSize },
    { name: "justification", label: "Justifications" },
  ];
  public bioFctTableCol = [
    { name: "type", label: "Fonctions biologiques", size: this.functionSize },
    { name: "qualification", label: "Qualifications", size: this.qualifSize },
    { name: "connaissance", label: "Connaissance", size: this.knowledgeSize },
    { name: "justification", label: "Justifications" },
  ];
  public intertesTableCol = [
    { name: "type", label: "Intérêts patrimoniaux", size: this.functionSize },
    { name: "qualification", label: "Qualifications", size: this.qualifSize },
    { name: "connaissance", label: "Connaissance", size: this.knowledgeSize },
    { name: "justification", label: "Justifications" },
  ];

  public corineTableCol = [
    { name: "biotope", label: "Corine Biotope", size: this.functionSize },
    { name: "etat", label: "État de conservation", size: this.qualifSize },
    { name: "cahier", label: "Cahier Habitats" },
    { name: "recouvrement", label: "Recouvrement de la ZH (%)", size: "5%" },
  ];

  public socioEcoTableCol = [
    {
      name: "type",
      label: "Valeurs socio-économiques",
      size: this.functionSize,
    },
    { name: "qualification", label: "Qualifications", size: this.qualifSize },
    { name: "connaissance", label: "Connaissance", size: this.knowledgeSize },
    { name: "justification", label: "Justifications" },
  ];
}
