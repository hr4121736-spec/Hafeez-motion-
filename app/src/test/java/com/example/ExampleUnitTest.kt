package com.example

import com.example.model.ActionType
import com.example.ui.screens.normalizeDigits
import org.junit.Assert.assertEquals
import org.junit.Test

class ExampleUnitTest {
    @Test
    fun testUrduDigitsNormalization() {
        val urduInput = "۲.۵, ۵.۰, ۷.۸"
        val normalized = normalizeDigits(urduInput)
        assertEquals("2.5, 5.0, 7.8", normalized)
    }

    @Test
    fun testActionTypeParsing() {
        assertEquals(ActionType.TAP, ActionType.fromString("tap"))
        assertEquals(ActionType.LONG_PRESS, ActionType.fromString("long_press"))
        assertEquals(ActionType.REQUEST_PERMISSION, ActionType.fromString("request_permission"))
        assertEquals(ActionType.WAIT, ActionType.fromString("unknown_action"))
    }
}
