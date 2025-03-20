from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class DerechosAutoriaWizard(models.TransientModel):
    """ Wizard: *** """
    _name = 'ddaa.wizard.descontrol'
    _description =  "Wizard Derechos Autoría"

    def generar_derechos_autoria(self):
        libros = self.env['product.template'].filtered(lambda p: self.env.company.is_category_genera_ddaa_or_child(p.categ_id))

        for libro in libros:
            _logger.debug(f"*********************Libro: {libro}")
            libro.write({'genera_ddaa': True})
            if not libro.author_name:
                _logger.warning(f"*********************Libro sin autoría: {libro.name}")
                continue
            product_product = self.env['product.product'].search([('product_tmpl_id', '=', libro.id)])

            # calcular libros vendidos menos libros devueltos
            domain_salida = [
                ('location_dest_id', '=', 5), # This is the id of the Location Partner Locations/Customers (the destination of the move)
                ('product_id', '=', product_product.id),
                ('state', '=', 'done')
            ]
            movimientos_salida = self.env['stock.move.line'].search(domain_salida)
            if not movimientos_salida:
                continue
            qty_salida = sum(m.qty_done for m in movimientos_salida)
            domain_entrada = [
                ('location_id', '=', 5), # This is the id of the Location Partner Locations/Customers (the source of the move)
                ('product_id', '=', product_product.id),
                ('state', '=', 'done')
            ]
            movimientos_entrada = self.env['stock.move.line'].search(domain_entrada)
            qty_entrada = 0
            if movimientos_entrada:
                qty_entrada_sum = sum(m.qty_done for m in movimientos_entrada)
                if qty_entrada_sum >= 0:
                    qty_entrada = qty_entrada_sum

            qty_ddaa = qty_salida - qty_entrada
            _logger.warning(f"*********************Libro con autoría {libro.author_name.name} y nombre {libro.name} genera ddaa: {qty_ddaa} ({qty_salida} - {qty_entrada})")

            if qty_ddaa <= 0:
                continue

            domain_purchase_order = [
                ('partner_id', '=', libro.author_name.id),
                ('state', '=', 'draft'),
                ('is_ddaa_order', '=', True)
            ]
            compra_derechos_autoria = self.env['purchase.order'].search(domain_purchase_order, order='date_order desc')
            if not compra_derechos_autoria:
                # crear sale.order a la autora
                compra_derechos_autoria = self.env['purchase.order'].create({
                    'partner_id': libro.author_name.id,
                    'is_ddaa_order': True
                })

            # crear producto derecho de autoría
            ddaa = libro.derecho_autoria
            if not ddaa:
                ddaa = self.env['product.template'].create({
                    'name': 'DDAA de ' + libro.name,
                    'categ_id': 4,
                    'list_price': libro.list_price * 0.1,
                    'type': 'service',
                    'sale_ok': False,
                    'purchase_ok': True,
                    'author_name': libro.author_name,
                    'producto_referencia': [libro.id],
                    'derecho_autoria': False
                })

            linea_libro_compra = compra_derechos_autoria.order_line.filtered(lambda line: line.product_id.product_tmpl_id.id == ddaa.id)
            if linea_libro_compra:
                linea_libro_compra[0].write({'product_qty': linea_libro_compra[0].product_qty +  qty_ddaa})
            else:
                product_id = self.env['product.product'].search([('product_tmpl_id', '=', ddaa.id)])
                vals = {
                    'name': ddaa.name,
                    'order_id': compra_derechos_autoria.id,
                    'product_id': product_id.id,
                    'product_qty': qty_ddaa,
                    'price_unit': ddaa.list_price,
                    'product_uom': 1,
                    'date_planned': compra_derechos_autoria.date_order,
                    'display_type': False
                }
                compra_derechos_autoria.write({'order_line': [(0,0,vals)]})
