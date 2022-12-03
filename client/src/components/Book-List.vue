<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Book</h1>
        <hr>
        <br><br>
        <alert :message="message"></alert>
        <rand></rand>
        <button type="button" class="btn btn-success btn-sm" data-bs-toggle="modal"
                data-bs-target="#book-modal">Add Book
        </button>
        <br><br>
        <table class="table table-hover">
          <thead>
          <tr>
            <th scope="col">Title</th>
            <th scope="col">Author</th>
            <th scope="col">Read?</th>
            <th></th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(book, index) in books" :key="index">
            <td>{{ book.title }}</td>
            <td>{{ book.author }}</td>
            <td>
              <span v-if="book.read">Yes</span>
              <span v-else>No</span>
            </td>
            <td>
              <div class="btn-group" role="group">
                <button type="button" class="btn btn-warning btn-sm" @click="editBook(book)"
                        data-bs-toggle="modal"
                        data-bs-target="#book-modal">Update
                </button>
                <button type="button" class="btn btn-danger btn-sm" @click="onDeleteBook(book)">
                  Delete
                </button>
              </div>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="modal fade" id="book-modal" tabindex="-1" aria-labelledby="addANewBook"
         aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add a new book</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"
                    aria-label="Close" id="close-book-modal"></button>
          </div>
          <div class="modal-body">
            <form @submit="onSubmit" @reset="onReset" class="w-100">
              <label for="form-title-input" class="form-label">Title:</label>
              <div class="form-group" id="form-title-group">
                <input id="form-title-input"
                       type="text"
                       v-model="bookForm.title"
                       required
                       placeholder="Enter title">
              </div>
              <label for="form-author-input" class="form-label">Author:</label>
              <div class="form-group" id="form-author-group">
                <input id="form-author-input"
                       type="text"
                       v-model="bookForm.author"
                       required
                       placeholder="Enter author">
              </div>
              <div class="check" id="form-read-group">
                <label class="form-check-label" for="form-checks">Read?</label>
                <input class="form-check-input" id="form-checks" v-model="bookForm.read"
                       type="checkbox" value="true">
              </div>
              <button type="reset" class="btn btn-danger"
                      data-bs-dismiss="modal">Close
              </button>
              <button type="submit" class="btn btn-primary">Save changes
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';
import Random from './Random.vue';

export default {
  data() {
    return {
      books: [],
      bookForm: {
        title: '',
        author: '',
        read: [],
      },
      message: '',
    };
  },
  components: {
    alert: Alert,
    rand: Random,
  },
  methods: {
    getBooks() {
      const path = 'http://localhost:5000/books';
      axios.get(path)
        .then((res) => {
          this.books = res.data.books;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addBook(payload) {
      const path = 'http://localhost:5000/books';
      axios.post(path, payload)
        .then(() => {
          this.getBooks();
          this.message = 'Book added!';
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getBooks();
        });
    },
    removeBook(bookID) {
      const path = `http://localhost:5000/books/${bookID}`;
      axios.delete(path)
        .then(() => {
          this.getBooks();
          this.message = 'Book removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getBooks();
        });
    },
    onDeleteBook(book) {
      this.removeBook(book.id);
    },
    updateBook(payload, bookID) {
      const path = `http://localhost:5000/books/${bookID}`;
      axios.put(path, payload)
        .then(() => {
          this.getBooks();
          this.message = 'Book updated!';
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getBooks();
        });
    },
    initForm() {
      this.bookForm.id = '';
      this.bookForm.title = '';
      this.bookForm.author = '';
      this.bookForm.read = [];
    },
    editBook(book) {
      this.bookForm = { ...book };
    },
    onSubmit(evt) {
      evt.preventDefault();
      document.getElementById('close-book-modal').click();
      let read = false;
      if (this.bookForm.read[0]) read = true;
      const payload = {
        title: this.bookForm.title,
        author: this.bookForm.author,
        read, // property shorthand
      };

      if (this.bookForm.id) {
        this.updateBook(payload, this.bookForm.id);
      } else {
        this.addBook(payload);
      }

      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      document.getElementById('close-book-modal').click();
      this.initForm();
    },
  },
  created() {
    this.getBooks();
  },
};
</script>
