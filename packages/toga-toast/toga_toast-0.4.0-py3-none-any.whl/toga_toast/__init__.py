def show_toast(self, message):
    from android.widget import Toast

    Toast.makeText(self._impl.native, message, Toast.LENGTH_SHORT).show()
