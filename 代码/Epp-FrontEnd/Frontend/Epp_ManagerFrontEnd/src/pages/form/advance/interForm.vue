<template>
<a-card :title="解读管理" :bordered="false">
  <form :autoFormCreate="(form) => this.form = form">
    <a-table
      :columns="columns"
      :dataSource="dataSource"
    >
    <div
      slot="filterDropdown"
      slot-scope="{ setSelectedKeys, selectedKeys, confirm, clearFilters, column }"
      style="padding: 8px"
    >
      <a-input
        v-ant-ref="c => (searchInput = c)"
        :placeholder="`Search ${column.dataIndex}`"
        :value="selectedKeys[0]"
        style="width: 188px; margin-bottom: 8px; display: block;"
        @change="e => setSelectedKeys(e.target.value ? [e.target.value] : [])"
        @pressEnter="() => handleSearch(selectedKeys, confirm, column.dataIndex)"
      />
      <a-button
        type="primary"
        icon="search"
        size="small"
        style="width: 90px; margin-right: 8px"
        @click="() => handleSearch(selectedKeys, confirm, column.dataIndex)"
      >
        Search
      </a-button>
      <a-button size="small" style="width: 90px" @click="() => handleReset(clearFilters)">
        Reset
      </a-button>
    </div>
    <a-icon
      slot="filterIcon"
      slot-scope="filtered"
      type="search"
      :style="{ color: filtered ? '#108ee9' : undefined }"
    />


      <template  v-for="(col, i) in ['name', 'number', 'department']" :slot="col" slot-scope="text, record">
          <a-input
            :key="col"
            v-if="record.editable"
            style="margin: -5px 0"
            :value="text"
            :placeholder="columns[i].title"
            @change="e => handleChange(e.target.value, record.key, col)"
          />
          <template v-else>{{text}}</template>
      </template>
      <template slot="operation" slot-scope="text, record">
        <template v-if="record.editable">
          <span v-if="record.isNew">
            <a @click="saveRow(record.key)">{{$t('add')}}</a>
            <a-divider type="vertical" />
            <a-popconfirm :title="$t('deleteConfirm')" @confirm="remove(record.key)">
              <a>{{$t('delete')}}</a>
            </a-popconfirm>
          </span>
            <span v-else>
            <a @click="saveRow(record.key)"><a-icon type="save"/>{{$t('save')}}</a>
            <a-divider type="vertical" />
            <a @click="cancle(record.key)"><a-icon type="close-circle"/>{{$t('cancel')}}</a>
          </span>
        </template>
        <span v-else>
          <a @click="toggle(record.key)"><a-icon type="edit"/>{{$t('edit')}}</a>
          <a-divider type="vertical" />
          <a-popconfirm :title="$t('deleteConfirm')" @confirm="remove(record.key)">
            <a><a-icon type="delete"/>{{$t('delete')}}</a>
          </a-popconfirm>
        </span>
      </template>
    </a-table>
    <a-button style="width: 100%; margin-top: 16px; margin-bottom: 8px" type="dashed" icon="plus" href="#/user/new">{{$t('newMember')}}</a-button>
  </form>
</a-card>
</template>

<script>
// const columns = [
//   {
//     title: '成员姓名',
//     dataIndex: 'name',
//     key: 'name',
//     width: '20%',
//     scopedSlots: { customRender: 'name' }
//   },
//   {
//     title: '工号',
//     dataIndex: 'number',
//     key: 'number',
//     width: '20%',
//     scopedSlots: { customRender: 'number' }
//   },
//   {
//     title: '所属部门',
//     dataIndex: 'department',
//     key: 'department',
//     width: '40%',
//     scopedSlots: { customRender: 'department' }
//   },
//   {
//     title: '操作',
//     key: 'operation',
//     scopedSlots: { customRender: 'operation' }
//   }
// ]

const dataSource = []
for (let i = 4; i < 100; i++) {
  dataSource.push({
    key: i.toString(),
    name: `Edrward ${i}`,
    age: 32,
    address: `London Park no. ${i}`,
  });
}

export default {
  name: 'UserForm',
  i18n: require('./i18n-user'),
  data () {
    return {
      dataSource,
      searchText: '',
      searchInput: null,
      searchedColumn: '',
      columns: [
        {
          title: 'Name',
          dataIndex: 'name',
          key: 'name',
          width: '20%',
          scopedSlots: {
            filterDropdown: 'filterDropdown',
            filterIcon: 'filterIcon',
            customRender: 'customRender',
          },
          onFilter: (value, record) =>
            record.name
              .toString()
              .toLowerCase()
              .includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: visible => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus();
              }, 0);
            }
          },
        },
        {
          title: 'Age',
          dataIndex: 'age',
          key: 'age',
          width: '20%',
          scopedSlots: {
            filterDropdown: 'filterDropdown',
            filterIcon: 'filterIcon',
            customRender: 'customRender',
          },
          onFilter: (value, record) =>
            record.age
              .toString()
              .toLowerCase()
              .includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: visible => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus();
              });
            }
          },
        },
        {
          title: 'Address',
          dataIndex: 'address',
          key: 'address',
          width: '40%',
          scopedSlots: {
            filterDropdown: 'filterDropdown',
            filterIcon: 'filterIcon',
            customRender: 'customRender',
          },
          onFilter: (value, record) =>
            record.address
              .toString()
              .toLowerCase()
              .includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: visible => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus();
              });
            }
          },
        },
        {
            title: '操作',
            key: 'operation',
            scopedSlots: { customRender: 'operation' }
        },
      ],
    }
  },
  // computed: {
  //   dataColumns() {
  //     return this.columns.map(column => {
  //       column.title = this.$t('table.' + column.key)
  //       return column
  //     })
  //   }
  // },
  methods: {
    handleSubmit (e) {
      e.preventDefault()
    },
    // newMember () {
    //   this.dataSource.push({
    //     key: this.dataSource.length + 1,
    //     name: '',
    //     number: '',
    //     department: '',
    //     editable: true,
    //     isNew: true
    //   })
    // },
    remove (key) {
      const newData = this.dataSource.filter(item => item.key !== key)
      this.dataSource = newData
    },
    saveRow (key) {
      let target = this.dataSource.filter(item => item.key === key)[0]
      target.editable = false
      target.isNew = false
    },
    toggle (key) {
      let target = this.dataSource.filter(item => item.key === key)[0]
      target.editable = !target.editable
    },
    getRowByKey (key, newData) {
      const data = this.dataSource
      return (newData || data).filter(item => item.key === key)[0]
    },
    cancle (key) {
      let target = this.dataSource.filter(item => item.key === key)[0]
      target.editable = false
    },
    handleChange (value, key, column) {
      const newData = [...this.dataSource]
      const target = newData.filter(item => key === item.key)[0]
      if (target) {
        target[column] = value
        this.dataSource = newData
      }
    },
    handleSearch(selectedKeys, confirm, dataIndex) {
      confirm();
      this.searchText = selectedKeys[0];
      this.searchedColumn = dataIndex;
    },

    handleReset(clearFilters) {
      clearFilters();
      this.searchText = '';
    },
  }
}
</script>

<style scoped>
.highlight {
  background-color: rgb(255, 192, 105);
  padding: 0px;
}
</style>
