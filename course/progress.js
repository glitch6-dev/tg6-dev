/* TG6-Dev · AI Training — progress tracking.
 *
 * Local-only for now: completed lesson IDs live in localStorage. When auth +
 * Stripe gating land, swap this module's storage for a per-user backend call;
 * the public API (Progress.*) stays the same so pages don't change.
 */
window.Progress = (function () {
  var KEY = "zts.progress.v1";
  var LAST_KEY = "zts.lastLesson.v1";

  function load() {
    try {
      var raw = localStorage.getItem(KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) {
      return {};
    }
  }

  function save(state) {
    try {
      localStorage.setItem(KEY, JSON.stringify(state));
    } catch (e) {
      /* storage unavailable (private mode) — progress just won't persist */
    }
  }

  function allLessonIds() {
    var ids = [];
    (window.CURRICULUM || []).forEach(function (m) {
      m.lessons.forEach(function (l) {
        ids.push(l.id);
      });
    });
    return ids;
  }

  return {
    isComplete: function (id) {
      return !!load()[id];
    },
    setComplete: function (id, done) {
      var state = load();
      if (done) state[id] = true;
      else delete state[id];
      save(state);
    },
    toggle: function (id) {
      var done = !this.isComplete(id);
      this.setComplete(id, done);
      return done;
    },
    /* { done, total, percent } across the whole course */
    summary: function () {
      var ids = allLessonIds();
      var state = load();
      var done = ids.filter(function (id) {
        return state[id];
      }).length;
      var total = ids.length;
      return {
        done: done,
        total: total,
        percent: total ? Math.round((done / total) * 100) : 0,
      };
    },
    /* remember / recall the last lesson opened, for "continue where you left off" */
    setLast: function (id) {
      try {
        localStorage.setItem(LAST_KEY, id);
      } catch (e) {}
    },
    getLast: function () {
      try {
        return localStorage.getItem(LAST_KEY);
      } catch (e) {
        return null;
      }
    },
    /* first lesson id in the course (fallback for "start" / "continue") */
    firstId: function () {
      var ids = allLessonIds();
      return ids.length ? ids[0] : null;
    },
    /* next uncompleted lesson, or null if everything is done */
    nextUnfinished: function () {
      var state = load();
      var ids = allLessonIds();
      for (var i = 0; i < ids.length; i++) {
        if (!state[ids[i]]) return ids[i];
      }
      return null;
    },
  };
})();
