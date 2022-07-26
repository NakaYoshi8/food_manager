// ダッシュボード
// カテゴリリスト
new Vue({
    el: '#dashboard-category',
    data: {
        isActive: false,
        btnText: '+',
    },
    methods: {
        changeShow() {
            this.isActive = !this.isActive;
            if (this.btnText==='+') {
                this.btnText = '-';
            } else {
                this.btnText = '+';
            }
        }
    },
})

// タグリスト
new Vue({
    el: '#dashboard-tag',
    data: {
        isActive: false,
        btnText: '+',
    },
    methods: {
        changeShow() {
            this.isActive = !this.isActive;
            if (this.btnText==='+') {
                this.btnText = '-';
            } else {
                this.btnText = '+';
            }
        }
    },
})

// 食品リスト
new Vue({
    el: '#dashboard-food',
    data: {
        isActive: false,
        btnText: '+',
    },
    methods: {
        changeShow() {
            this.isActive = !this.isActive;
            if (this.btnText==='+') {
                this.btnText = '-';
            } else {
                this.btnText = '+';
            }
        }
    },
})

// 各カテゴリページ
new Vue({
    el: '#category-heading',
    data: {
        isActive: false,
    },
    methods: {
        changeShow() {
            this.isActive = !this.isActive;
        }
    },
})

// 各タグページ
new Vue({
    el: '#tag-heading',
    data: {
        isActive: false,
    },
    methods: {
        changeShow() {
            this.isActive = !this.isActive;
        }
    },
})

// 各食品ページ
new Vue({
    el: '#food-heading',
    data: {
        editFormIsActive: false,
        trashModalIsActive: false,
    },
    methods: {
        changeShowEditForm() {
            this.editFormIsActive = !this.editFormIsActive;
        },
        openTrashModal() {
            this.trashModalIsActive = true;
        },
        closeTrashModal() {
            this.trashModalIsActive = false;
        },
    },
})

// ごみ箱ページ
// 1つ以上にチェックがついている場合は、ボタンを活性化
// 1つもついていない場合は、ボタンを非活性化
/* new Vue({
    el: '#trashed-food-list',
    data: {

    },
    methods: {
        
    },
}) */