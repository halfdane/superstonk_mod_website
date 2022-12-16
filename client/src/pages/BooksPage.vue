<template>

  <h1>Book</h1>
  <hr>
  <br><br>
  <alert-success :message="message"></alert-success>
  <q-btn color="primary" label="Add Book" @click="edit_dialog = true"/>

  <br><br>

  <q-table
    title="Treats"
    :columns="columns"
    :rows="books"
    row-key="name"
  >
    <template v-slot:body="props">
      <q-tr :props="props">
        <q-td key="title" :props="props">
          {{ props.row.title }}
        </q-td>
        <q-td key="author" :props="props">
          {{ props.row.author }}
        </q-td>
        <q-td key="read" :props="props">
          <q-badge :color="props.row.read ? 'green' : 'red'">
            <span v-if="props.row.read">Yes</span>
            <span v-else>No</span>
          </q-badge>
        </q-td>
        <q-td key="id" :props="props">
          <q-btn-group push>
            <q-btn name="update" label='Update' icon='update' push @click="editBook(props.row); edit_dialog = true"/>
            <q-btn name="delete" color="red" label='delete' icon='delete' push @click="onDeleteBook(props.row)"/>
          </q-btn-group>
        </q-td>
      </q-tr>
    </template>
  </q-table>

  <q-dialog v-model="edit_dialog">
    <q-card style="width: 700px; max-width: 80vw;">

      <q-avatar icon="edit" color="primary" text-color="white"/>
      <span class="q-ml-sm">Add a new book</span>

      <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
        <q-card-section class="row items-center">

          <q-input
            filled
            v-model="bookForm.title"
            label="Title *"
            stack-label
            hint="The title of the book"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type something']"
          />
        </q-card-section>
        <q-card-section class="row items-center">
          <q-input
            filled
            v-model="bookForm.author"
            label="The book's author *"
            stack-label
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type something']"
          />
        </q-card-section>

        <q-card-section class="row items-center">
          <q-toggle v-model="bookForm.read" label="I have read the book"/>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn label="Submit" type="submit" color="primary" v-close-popup/>
          <q-btn label="Reset" type="reset" color="primary" v-close-popup/>
        </q-card-actions>
      </q-form>
    </q-card>
  </q-dialog>
</template>

<script>
import AlertSuccess from '../components/AlertSuccess'
import { ref } from 'vue'

export default {
  setup () {
    return {
      edit_dialog: ref(false)
    }
  },
  data () {
    return {
      columns: [
        { name: 'title', align: 'left', label: 'Title', field: 'title', sortable: true },
        { name: 'author', align: 'left', label: 'Author', field: 'author', sortable: true },
        { name: 'read', label: 'Read ?', field: 'read', sortable: true },
        { name: 'id', align: 'center', label: 'Action', field: 'id', sortable: true }
      ],
      books: [],
      bookForm: {
        title: '',
        author: '',
        read: ref(true)
      },
      message: ''
    }
  },
  components: {
    AlertSuccess
  },
  methods: {
    getBooks () {
      const path = 'http://localhost:5000/books'
      fetch(path)
        .then((response) => response.json())
        .then((data) => {
          this.books = data.books
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        })
    },
    addBook (payload) {
      const path = 'http://localhost:5000/books'
      const options = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      }
      fetch(path, options)
        .then(() => {
          this.getBooks()
          this.message = 'Book added!'
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.getBooks()
        })
    },
    removeBook (bookID) {
      const path = `http://localhost:5000/books/${bookID}`
      fetch(path, { method: 'DELETE' })
        .then(() => {
          this.getBooks()
          this.message = 'Book removed!'
          this.showMessage = true
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.getBooks()
        })
    },
    onDeleteBook (book) {
      this.removeBook(book.id)
    },
    updateBook (payload, bookID) {
      const path = `http://localhost:5000/books/${bookID}`
      const options = {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      }
      console.log(payload)
      console.log(options)
      fetch(path, options)
        .then(() => {
          this.getBooks()
          this.message = 'Book updated!'
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.getBooks()
        })
    },
    initForm () {
      this.bookForm.id = ''
      this.bookForm.title = ''
      this.bookForm.author = ''
      this.bookForm.read = false
    },
    editBook (book) {
      this.bookForm = { ...book }
    },
    onSubmit (evt) {
      evt.preventDefault()
      const payload = {
        title: this.bookForm.title,
        author: this.bookForm.author,
        read: this.bookForm.read
      }

      if (this.bookForm.id) {
        this.updateBook(payload, this.bookForm.id)
      } else {
        this.addBook(payload)
      }

      this.initForm()
    },
    onReset (evt) {
      evt.preventDefault()
      this.initForm()
    }
  },
  created () {
    this.getBooks()
  }
}

</script>
