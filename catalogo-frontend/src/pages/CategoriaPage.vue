<template>
  <q-page padding>
    <!-- content -->

    <!-- Listado -->
    <section v-if="view === 'list'">
      <!-- <pre> {{ pagination }} </pre> -->
      <q-table
        title="Catálogo"
        :rows="rows"
        :columns="columns"
        :loading="loading"
        :filter="filter"
        v-model:pagination="pagination"
        @request="val => onRequest(val)">
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
              <!-- <pre>{{ props }}</pre> -->
              <div v-if="col.name === 'acciones'">
                <q-btn round flat icon="edit" color="primary" :disable="loading" :loading="loading"
                  @click.prevent="onEdit(props.row)">
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
            <div v-if="view === 'add'" class="text-h6">Agregar Categoría</div>
            <div v-else class="text-h6">Editar Categoría</div>
            <div class="text-subtitle2">Complete los campos del formulario</div>
          </q-card-section>

          <q-card-section>
            <q-input v-model="categoria.descripcion" label="Nombre de la Categoría *" filled
              :rules="[val => val && val.length > 0 || 'El campo es requerido']" />
          </q-card-section>

          <q-separator />
          <q-card-actions align="around">
            <q-btn flat @click.prevent="(val) => { view = 'list' }">Volver</q-btn>
            <q-btn flat type="submit" :loading="loading" color="positive">{{ view === 'add' ? 'Grabar' :
              'Editar'}}</q-btn>
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
            esta Categoría
            <strong>{{ categoria.descripcion }}</strong>
          </span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancelar" v-close-popup />
          <q-btn flat label="Eliminar" color="negative" @click.prevent="deleteCategoria(categoria)"
            :loading="loading" />
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
  name: "CategoriaPage",
  components: [],
  props: {},
  emits: [],
  setup(props, contexto) {
    // Propiedades
    const $q = useQuasar()
    const columns = [
      {
        name: "descripcion",
        label: "Descripción",
        align: "left",
        field: (row) => row.descripcion,
        sortable: true,
      },
      {
        name: "acciones",
        label: "Acciones",
        align: "center"
      }
    ];

    const pagination = ref({
      sortBy: 'descripcion',
      descending: false,
      page: 1,
      rowsPerPage: 5
      // rowsNumber: xx if getting data from a server
    })

    const rows = ref([]);
    const loading = ref(false);
    const filter = ref("");
    const view = ref("list");
    const confirm = ref(false);

    const onClearCategoria = () => {
      return {
        id: null,
        descripcion: null
      }
    }
    const categoria = ref(onClearCategoria);

    // Metodos
    const updatePagination = (newPagination, total) => {
      const { page, rowsPerPage, sortBy, descending } = newPagination
      pagination.value.page = page
      pagination.value.rowsPerPage = rowsPerPage
      pagination.value.sortBy = sortBy
      pagination.value.descending = descending
      pagination.value.rowsNumber = total
    }

    const onRequest = (props) => {
      console.log(props)

      const { page, rowsPerPage, sortBy, descending } = props.pagination
      const filter = props.filter

      // Merge params in object for backend
      const paramsBackend = {
        page,
        rowsPerPage,
        sortBy,
        descending,
        jsondepth: 1
      }

      const dataFilter = {
        descripcion: filter
      }

      loading.value = true
      axios.post('http://127.0.0.1:5000/api/search/categorias', dataFilter, { params: paramsBackend })
        .then((response) => {
          rows.value = response.data.items
          updatePagination(props.pagination, response.data.total)
        }).catch((error) => {
          console.log(error)
        }).finally(() => {
          loading.value = false
        })
    }

    const onAdd = () => {
      view.value = 'add'
      categoria.value = onClearCategoria()
    }

    const onEdit = (filaInstancia) => {
      view.value = 'edit'
      categoria.value = filaInstancia
    }

    const onDelete = (filaInstancia) => {
      confirm.value = true  // Mostrar el modal de eliminacion
      categoria.value = filaInstancia
    }

    const onSubmit = () => {
      loading.value = true

      //1. Saber que es? adicion o modificacion
      if (categoria.value.id) {
        // Edicion
        axios.put(`http://localhost:5000/api/categorias/${categoria.value.id}`, categoria.value)
          .then((response) => {
            console.log(response)

            // Ir al listado y actualizar lista
            view.value = 'list'
            onRequest({
              pagination: pagination.value,
              filter: filter.value
            })

            // Mostrar un mensaje de exito
            $q.notify({
              message: 'La categoría se ha modificado',
              color: 'positive'
            })
          }).catch((error) => {
            console.log(error)
            // Mostrar un mensaje de exito
            $q.notify({
              message: 'La categoría NO se ha modificado.',
              color: 'negative'
            })
          }).finally(() => {
            loading.value = false
          })
      } else {
        // Adición
        axios.post('http://localhost:5000/api/categorias', categoria.value)
          .then((response) => {
            console.log(response)

            // Ir al listado y actualizar lista
            view.value = 'list'
            onRequest({
              pagination: pagination.value,
              filter: filter.value
            })

            // Mostrar un mensaje de exito
            $q.notify({
              message: 'La categoría se ha creado',
              color: 'positive'
            })
          }).catch((error) => {
            console.log(error)
            // Mostrar un mensaje de exito
            $q.notify({
              message: 'La categoría NO se ha creado.',
              color: 'negative'
            })
          }).finally(() => {
            loading.value = false
          })
      }
    }

    const deleteCategoria = (filaInstancia) => {
      loading.value = true
      axios.delete(`http://localhost:5000/api/categorias/${filaInstancia.id}`)
        .then((response) => {
          console.log(response)

          // Cerrar el modal y actualizar lista
          confirm.value = false
          onRequest({
              pagination: pagination.value,
              filter: filter.value
            })

          // Mostrar un mensaje de exito
          $q.notify({
            message: 'La categoría se ha elimiando',
            color: 'positive'
          })
        }).catch((error) => {
          console.log(error)
          // Mostrar un mensaje de exito
          $q.notify({
            message: 'La categoría NO se ha eliminado.',
            color: 'negative'
          })
        }).finally(() => {
          loading.value = false
        })
    }

    // Metodos del ciclo de vida del componente
    onMounted(() => {
      onRequest({
        pagination: pagination.value,
        filter: filter.value
      })
    })

    return {
      rows,
      columns,
      loading,
      onRequest,
      filter,
      onAdd,
      view,
      onSubmit,
      categoria,
      onEdit,
      confirm,
      onDelete,
      deleteCategoria,
      pagination
    };
  },
};
</script>
