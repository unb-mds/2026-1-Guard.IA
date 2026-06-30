import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.coleta import coletor_camara


class ColetorCamaraTests(unittest.TestCase):
    def test_buscar_detalhes_proposicao_extrae_estado_do_autor(self):
        mock_response = {
            "dados": [
                {
                    "id": 12345,
                    "nome": "Maria Souza",
                    "siglaPartido": "PSOL",
                    "siglaUf": "DF",
                    "uri": "https://dadosabertos.camara.leg.br/api/v2/deputados/99999",
                }
            ]
        }

        with patch("app.coleta.coletor_camara.requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_response
            mock_get.return_value.raise_for_status.return_value = None

            detalhes = coletor_camara.buscar_detalhes_proposicao(12345)

        self.assertEqual(detalhes["autor"], "Maria Souza")
        self.assertEqual(detalhes["partido"], "PSOL")
        self.assertEqual(detalhes["estado"], "DF")


if __name__ == "__main__":
    unittest.main()
