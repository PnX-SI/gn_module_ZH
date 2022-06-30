import { Injectable } from "@angular/core";

type error = {
  api: string;
  front: string;
  id: number;
};

@Injectable({
  providedIn: "root",
})
export class ErrorTranslatorService {
  constructor() {}

  private errors = [
    {
      api: "polygon_contained_in_zh", // error returned by backend
      front: "La geometrie est contenue entièrement dans une autre zone humide", //error to show to the user
      id: 1,
    },
    {
      api: "ZH_main_name_already_exists",
      front:
        "Impossible de créer un identifiant unique avec les informations entrées. Le nom est peut-être déjà pris ?",
      id: 2,
    },
    {
      api: "set_geom_error",
      front: "Impossible de créer la géométrie, elle ne semble pas appropriée",
      id: 3,
    },
    {
      api: "wrong_qualif",
      front:
        "La typologie SDAGE selectionnée ne fait pas partie des règles définies pour ce bassin versant",
      id: 4,
    },
    {
      api: "post_cor_zh_rb_db_error",
      front: "Veuillez tracer une zone humide sur la carte",
      id: 5,
    },
    {
      api: "Hierarchy class: get_rb_error",
      front:
        "Impossible d'effectuer la hierarchisation car la zone humide ne se situe sur aucun bassin versant",
      id: 6,
    },
    {
      api: "csv_taxa_error",
      front: "Impossible de générer le csv des espèces",
      id: 7,
    },
    {
      api: "no_rb_rules",
      front: "Il n'existe pas de règle pour ce bassin versant",
      id: 8,
    },
    {
      api: "no_river_basin",
      front: "Cette zone humide n'intersecte aucun bassin versant",
      id: 9,
    },
    {
      api: "user_not_allowed",
      front: "Vous n'avez pas les droits pour supprimer/modifier/lire cette zone humide",
      id: 10,
    },
    {
      api: "get_file_list_error",
      front:
        "Impossible de récupérer la liste des fichiers sur cette zones humides, erreur serveur",
      id: 11,
    },
    {
      api: "upload_file_patch_error",
      front: "Impossible de mettre à jour ce fichier. Erreur serveur",
      id: 12,
    },
    {
      api: "delete_one_file_error",
      front: "Impossible de supprimer ce fichier. Erreur serveur",
      id: 13,
    },
    {
      api: "download_file_error",
      front: "Impossible de télécharger ce fichier. Erreur serveur",
      id: 14,
    },
    {
      api: "filter_zh_error",
      front: "Impossible de récupérer/filtrer les zones humides. Erreur serveur",
      id: 15,
    },
    {
      api: "empty_geometry",
      front: "Veuillez tracer une geométrie",
      id: 16,
    },
    {
      api: "Forbidden",
      front: "Vous ne possedez pas les droits pour effectuer cela",
      id: 17,
    },
  ];

  getError(errorMsg: string): error {
    const frontError: error = this.errors.filter((item) => item.api == errorMsg)[0];
    return frontError;
  }

  getFrontError(errorMsg: string): string {
    console.log("error:", errorMsg);
    const frontError: error = this.getError(errorMsg);
    console.log(frontError);
    return frontError ? frontError.front : "Erreur inconnue";
  }

  getErrorId(errorMsg: string): number {
    const frontError: error = this.getError(errorMsg);
    return frontError ? frontError.id : 999999;
  }
}
