<template>
  <q-page padding>
    <!-- content -->

    <!-- Listado -->
    <section v-if="view === 'list'">
      <q-table title="Producto" :rows="rows" :columns="columns" :loading="loading" :filter="filter">
        <template v-slot:top-right>
          <q-input outlined dense filled label="Buscar..." debounce="300" color="positive" v-model="filter">
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
          <q-btn label="Agregar" outline icon="add" color="positive" :disable="loading" :loading="loading"
            class="q-ml-sm" @click.prevent="onAdd" />
          <q-space />
        </template>

        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td :props="props" v-for="col in props.cols" :key="col.name">
              <div v-if="col.name === 'acciones'">
                <q-btn round flat icon="edit" color="primary" :disable="loading" :loading="loading" @click.prevent="onEdit(props.row)">
                  <q-tooltip>Editar</q-tooltip>
                </q-btn>
                <q-btn round flat icon="delete" color="negative" :disable="loading" :loading="loading"
                  @click.prevent="onDelete(props.row)">
                  <q-tooltip>Eliminar</q-tooltip>
                </q-btn>
              </div>
              <div v-else> {{ col.value }}</div>
            </q-td>
          </q-tr>
        </template>

      </q-table>
    </section>

    <!-- Agregar -->
    <section v-if="view === 'add' || view === 'edit'">
      <q-form @submit="onSubmit">
        <q-card>
          <q-card-section>
            <div v-if="view === 'add'" class="text-h6">Agregar Producto</div>
            <div v-else class="text-h6">Editar Producto</div>
            <div class="text-subtitle2">Complete los datos del formulario</div>
          </q-card-section>

          <q-card-section>
            <q-input
              v-model="producto.nombre"
              label="Nombre del producto *"
              filled
              :rules="[ val => val && val.length > 0 || 'El campo es requerido']"
            />

            <q-input
              v-model="producto.descripcion"
              label="Descripción del producto *"
              filled
              :rules="[ val => val && val.length > 0 || 'El campo es requerido']"
            />

            <q-input
              v-model="producto.precio"
              label="Precio del producto"
              filled bottom-slots
            />

            <q-select
              v-model="producto.estado"
              :options="['Activo', 'Inactivo']"
              label="Estado"
              bottom-slots filled />
            <!-- <q-input
              v-model="producto.estado"
              label="Estado del producto *"
              filled
              :rules="[ val => val && val.length > 0 || 'El campo es requerido']"
            /> -->

            <q-select
              v-model="producto.categoria_id"
              :options="categoriaList"
              label="Categoría"
              option-label="descripcion"
              option-value="id" map-options emit-value
              bottom-slots filled />
            <!-- <q-input
              bottom-slots
              v-model="producto.categoria_id"
              label="Categoría del producto"
              filled
            /> -->

            <q-select
              v-model="producto.proveedor_id"
              :options="proveedorList"
              label="Proveedor"
              option-label="nombre"
              option-value="id" map-options emit-value
              bottom-slots filled />
            <!-- <q-input
              bottom-slots
              v-model="producto.proveedor_id"
              label="Proveedor del producto"
              filled
            /> -->
          </q-card-section>

          <q-separator />
          <q-card-actions align="around">
            <q-btn flat @click.prevent="(val) => { view = 'list' }">Volver</q-btn>
            <q-btn flat type="submit" :loading="loading" color="positive">{{view === 'add'? 'Grabar' : 'Editar'}}</q-btn>
          </q-card-actions>
        </q-card>
      </q-form>
    </section>

     <!-- Modales -->
     <q-dialog v-model="confirm" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="delete" color="negative" text-color="white" />
          <span class="q-ml-sm">
            Esta seguro de que desea
            <strong style="color:red">Eliminar</strong>
            este Producto
            <strong>{{ producto.nombre }}</strong>
          </span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancelar" v-close-popup />
          <q-btn flat label="Eliminar" color="negative" @click.prevent="deleteProducto(producto)" :loading="loading"/>
        </q-card-actions>
      </q-card>
    </q-dialog>

  </q-page>
</template>

<script>
import { onMounted, ref } from "vue"
import axios from 'axios'
import { useQuasar } from 'quasar'

export default {
  name: "ProductoPage",
  components: [],
  props: {},
  emits: [],
  setup(props, contexto) {
    const columns = [
      // { name: 'imagen', align: 'center', label: 'Imagen', field: row => row.imagen, sortable: true },
      { name: 'nombre', align: 'left', label: 'Nombre', field: row => row.nombre, sortable: true },
      { name: 'descripcion', align: 'left', label: 'Descripcion', field: row => row.descripcion, sortable: true },
      { name: 'precio', align: 'left', label: 'Precio', field: row => row.precio, sortable: true },
      { name: 'estado', align: 'left', label: 'Estado', field: row => row.estado, sortable: true },
      { name: 'proveedor', align: 'left', label: 'Proveedor', field: row => row._proveedor?.nombre, sortable: true },
      { name: 'categoria', align: 'left', label: 'Categoria', field: row => row._categoria?.descripcion, sortable: true },
      { name: "acciones", label: "Acciones", align: "center" }
    ]

    const $q = useQuasar()
    const rows = ref([]);
    const loading = ref(false);
    const filter = ref("");
    const view = ref("list");
    const confirm = ref(false);
    const categoriaList = ref([]);
    const proveedorList = ref([]);

    // Metodos
    const onRequest = () => {
      loading.value = true
      axios.get('http://127.0.0.1:5000/api/productos').then((response) => {
        rows.value = response.data
      }).catch((error) => {
        console.log(error)
      }).finally(() => {
        loading.value = false
      })
    }

    const onClearProducto = () => {
      return {
        id: null,
        nombre: null,
        descripcion: null,
        precio: null,
        estado: null,
        proveedor_id: null,
        categoria_id: null,
      }
    }
    const producto = ref(onClearProducto);

    const onAdd = () => {
      view.value = 'add'
      producto.value = onClearProducto()
    }

    const onEdit = (filaInstancia) => {
      view.value = 'edit'
      producto.value = filaInstancia
    }

    const onDelete = (filaInstancia) => {
      console.log(filaInstancia)
      confirm.value = true  // Mostrar el modal de eliminacion
      producto.value = filaInstancia
    }

    const onSubmit = () => {
      loading.value = true

      //1. Saber que es? adicion o modificacion
      if (producto.value.id) {
        // Edicion
        axios.put(`http://localhost:5000/api/productos/${producto.value.id}`, producto.value)
          .then((response) => {
            console.log(response)

            // Ir al listado y actualizar lista
            view.value = 'list'
            onRequest()

            // Mostrar un mensaje de exito
            $q.notify({
              message: 'El Producto se ha modificado',
              color: 'positive'
            })
          }).catch((error) => {
            console.log(error)
            // Mostrar un mensaje de exito
            $q.notify({
              message: 'El Producto NO se ha modificado.',
              color: 'negative'
            })
          }).finally(() => {
            loading.value = false
          })
      } else {
        // Adición
        axios.post('http://localhost:5000/api/productos', producto.value)
          .then((response) => {
            console.log(response)

            // Ir al listado y actualizar lista
            view.value = 'list'
            onRequest()

            // Mostrar un mensaje de exito
            $q.notify({
              message: 'El Producto se ha creado',
              color: 'positive'
            })
          }).catch((error) => {
            console.log(error)
            // Mostrar un mensaje de exito
            $q.notify({
              message: 'El Producto NO se ha creado.',
              color: 'negative'
            })
          }).finally(() => {
            loading.value = false
          })
      }
    }

    const deleteProducto = (filaInstancia) => {
      loading.value = true
      axios.delete(`http://localhost:5000/api/productos/${filaInstancia.id}`)
          .then((response) => {
            console.log(response)

            // Cerrar el modal y actualizar lista
            confirm.value = false
            onRequest()

            // Mostrar un mensaje de exito
            $q.notify({
              message: 'El Producto se ha elimiando',
              color: 'positive'
            })
          }).catch((error) => {
            console.log(error)
            // Mostrar un mensaje de exito
            $q.notify({
              message: 'El Producto NO se ha eliminado.',
              color: 'negative'
            })
          }).finally(() => {
            loading.value = false
          })
    }

    // Metodos del ciclo de vida del componente
    onMounted(async () => {
      onRequest()

      // Cargar opciones de selectores
      categoriaList.value = (await axios.get('http://127.0.0.1:5000/api/categorias')).data
      proveedorList.value = (await axios.get('http://127.0.0.1:5000/api/proveedores')).data
    })

    return {
      rows,
      columns,
      onRequest,
      loading,
      filter,
      onAdd,
      view,
      onSubmit,
      producto,
      onEdit,
      confirm,
      onDelete,
      deleteProducto,
      categoriaList,
      proveedorList
    }
  }
}
</script>
